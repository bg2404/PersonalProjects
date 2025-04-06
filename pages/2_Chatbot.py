import streamlit as st
from openai import RateLimitError, APIError, BadRequestError
import traceback
import time # Kept for potential re-introduction of sleep

try:
    from models.llm import TEXT_MODEL_OPTIONS
    from widgets.sidebar import setup_sidebar
except ImportError as e:
    st.error(f"Failed to import project modules: {e}")
    st.stop()

st.set_page_config(page_title="Chatbot", page_icon="💬")

try:
    selected_model_name, client = setup_sidebar(TEXT_MODEL_OPTIONS)
    if client is None:
        st.error("Failed to retrieve API client from sidebar setup.")
        st.stop()
except Exception as e:
    st.error("An error occurred during sidebar setup.")
    st.exception(e)
    st.stop()

st.title("💬 Chatbot")
st.caption(f"🚀 Powered by {selected_model_name}")

if "chatbot_messages" not in st.session_state:
    st.session_state["chatbot_messages"] = [
        {"role": "assistant", "content": "How can I help you?"}
    ]

for msg in st.session_state.chatbot_messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.chatbot_messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    api_messages = st.session_state.chatbot_messages

    try:
        response_stream = client.chat.completions.create(
            model=selected_model_name,
            messages=api_messages,
            stream=True,
        )

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for chunk in response_stream:
                if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    message_placeholder.markdown(full_response + "▌")
                    # time.sleep(0.01) # Optional: small delay for smoother visual effect

            message_placeholder.markdown(full_response)

        st.session_state.chatbot_messages.append({"role": "assistant", "content": full_response})

    except RateLimitError as e:
        st.error(f"API Rate Limit Error: Please wait and try again. {e}")
    except APIError as e:
        st.error(f"API Error: {e.status_code} - {e.message}")
    except BadRequestError as e:
         st.error(f"API Request Error: {e.message}")
    except Exception as e:
        st.error(f"An unexpected error occurred during the API call: {e}")
        # traceback.print_exc() # For debugging in console if needed
