import streamlit as st
from openai import APIError, BadRequestError, RateLimitError

from utils.load_json import load_news_articles

try:
    from models.llm import TEXT_MODEL_OPTIONS
    from widgets.sidebar import SidebarManager
except ImportError as e:
    st.error(f"Failed to import project modules: {e}")
    st.stop()

st.set_page_config(page_title="Artice Generator", page_icon="📰")

try:
    selected_model_name, client = SidebarManager(TEXT_MODEL_OPTIONS).setup()
    if client is None:
        st.error("Failed to retrieve API client from sidebar setup.")
        st.stop()
except Exception as e:
    st.error("An error occurred during sidebar setup.")
    st.exception(e)
    st.stop()

personas_data = load_news_articles()
personas = {persona["name"]: persona for persona in personas_data["personas"]}


def generate_prompt(topic, persona_name, additional_context=None):
    """
    Generates a prompt for the LLM to create an article based on a persona.

    Args:
        topic (str): The topic of the article.
        persona_name (str): The name of the persona of the article.
        additional_context (str): Additional context to derive the article details from.

    Returns:
        str: The generated prompt.
    """
    persona = personas.get(persona_name)
    use_examples = persona is not None

    prompt = f"""
    **Objective:**
    * Write a concise, engaging article in the style of Finshots.
    * Begin with a compelling question or scenario to hook the reader.
    * Use a conversational tone, simplifying complex financial or business topics into relatable narratives.
    * Don't make bullet points or lists; instead, weave the information into a narrative.
    * Incorporate real-world analogies and examples to elucidate key points.
    * Structure the article with a clear introduction, body, and conclusion, ensuring it can be read in under six minutes.
    * Where appropriate, include relevant data or visuals to support the content.
    * Maintain a tone that is informative yet accessible, aiming to make the subject matter understandable to readers without a financial background.

    **Content:** The Article should be about {topic}.
    """

    if use_examples:
        prompt = f"**Persona:** You are writing as {persona_name}.\n" + prompt
        prompt += """
        **Examples of articles by finshots. (Write articles in the same style as the examples below):**
        """
        for article in persona.get("articles", []):
            prompt += f"""
            - **Title:** {article["title"]}
              **Content:** {article["content"]}
            """
    else:
        prompt = f"**Persona:** Write in the style of {persona_name}.\n" + prompt

    prompt += """
    **Instructions:**
    - Use the following format to generate the article:
      **Title:** Example Title
      **Content:** Example content for the article.
    """

    if additional_context:
        prompt += f"""
        **Generate the article using following as a source of truth:**
        {additional_context}
        """
    return prompt.strip()  # Remove leading/trailing whitespaces


st.title("📰 Article Generator")
st.caption(f"🚀 Powered by {selected_model_name}")

st.write("### Article Generation Inputs")
topic = st.text_input("Enter the topic of the article:", "The Future of AI")
persona_name = st.selectbox("Select a persona:", personas.keys())
additional_context = st.text_area("Additional context (optional):")

if st.button("Generate Article"):
    if client is None:
        st.error("API Client not available. Please check configuration.")
        st.stop()

    prompt = generate_prompt(topic, persona_name, additional_context)

    with st.spinner("Generating article..."):
        try:
            response = client.chat.completions.create(
                model=selected_model_name,
                messages=[{"role": "user", "content": prompt}],
                # max_tokens=1024,
            )
            article_content = response.choices[0].message.content
            st.markdown(article_content, unsafe_allow_html=True)
            st.divider()
            st.write(len(article_content))

        except RateLimitError as e:
            st.error(f"API Rate Limit Error: {e}")
        except BadRequestError as e:
            st.error(f"API Request Error: {e.message}")
        except APIError as e:
            st.error(f"API Error: {e.message}")
        except Exception as e:
            st.error(f"An unexpected error occurred during the API call: {e}")
