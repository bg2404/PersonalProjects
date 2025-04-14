import traceback

import streamlit as st
from openai import APIError, BadRequestError, NotFoundError, RateLimitError

from utils.db_handler import DatabaseHandler
from utils.generate_prompt import generate_prompt
from utils.load_json import load_content_formats, load_content_types, load_personalities
from utils.post import SocialMediaPoster

try:
    from models.llm import TEXT_MODEL_OPTIONS
    from widgets.sidebar import SidebarManager
except ImportError as e:
    st.error(f"Failed to import project modules: {e}")
    st.stop()

st.set_page_config(page_title="Tweet Generator", page_icon="📲")

try:
    selected_model_name, client = SidebarManager(TEXT_MODEL_OPTIONS).setup()
    if client is None:
        st.error("Failed to retrieve API client from sidebar setup.")
        st.stop()
except Exception as e:
    st.error("An error occurred during sidebar setup.")
    st.exception(e)
    st.stop()

st.title("📲 Tweet Generator")
st.caption(f"🚀 Generate tweets using {selected_model_name}")

st.divider()

st.write("### Tweet Generation Inputs")
col1, col2, col3 = st.columns([2, 2, 1])
personality = col1.selectbox("Select personality type:", load_personalities().keys(), index=0)
content_type = col2.selectbox("Select content type:", load_content_types().keys(), index=0)
content_format = col3.selectbox("Select content format:", load_content_formats().keys(), index=0)
if content_format.lower() != "text":
    st.error("Currently, only text format is supported for tweet generation.")
    st.stop()

text_prompt = generate_prompt(
    personality=personality,
    content_type=content_type,
    content_format=content_format,
)

if "content_generated" not in st.session_state:
    st.session_state["content_generated"] = False
if "model_response" not in st.session_state:
    st.session_state["model_response"] = ""


def generate_content():
    st.session_state["content_generated"] = True
    if client is None:
        st.error("API Client not available. Please check configuration.")
        st.stop()

    content_payload = []
    if text_prompt:
        content_payload.append({"type": "text", "text": text_prompt})

    if content_payload:
        with st.spinner("Sending query to model..."):
            try:
                response = client.chat.completions.create(
                    model=selected_model_name,
                    messages=[
                        {
                            "role": "user",
                            "content": content_payload,
                        }
                    ],
                    max_tokens=1024,
                )
                model_response_content = response.choices[0].message.content
                st.session_state["model_response"] = model_response_content

            except RateLimitError as e:
                st.error(f"API Rate Limit Error: {e}")
            except NotFoundError as e:
                st.error(
                    f"Model Not Found Error: '{selected_model_name}' may not be available or support multimodal input. {e}"
                )
            except BadRequestError as e:
                st.error(f"API Request Error: {e.message}")
            except APIError as e:
                st.error(f"API Error: {e.message}")
            except Exception as e:
                st.error(f"An unexpected error occurred during the API call: {e}")
                traceback.print_exc()  # For debugging in console if needed


if st.button("Generate Content"):
    generate_content()

st.divider()

if st.session_state["content_generated"]:
    model_response = st.session_state["model_response"]
    st.write("### Generated Tweet:")
    st.markdown(model_response)

    db_handler = DatabaseHandler()

    if st.button("Post"):
        try:
            from utils.api_config import X_API

            XPoster = SocialMediaPoster("X", api_config=X_API)
            if tweet_status := XPoster.post(model_response):
                if type(tweet_status) is str:
                    st.success(f"✅ Tweet posted! [View on X]({tweet_status})")
                else:
                    st.success("✅ Tweet posted!")
                tweet_id = db_handler.add_tweet(
                    model_name=selected_model_name,
                    personality=personality,
                    content_type=content_type,
                    content_format=content_format,
                    tweet_text=model_response,
                    posted_url=tweet_status if type(tweet_status) is str else "posted",
                )
            else:
                st.error("Failed to post tweet.")
        except Exception as e:
            st.error(f"Failed to post tweet: {e}")
            traceback.print_exc()  # For debugging in console if needed
            st.stop()
