import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
from models.llm import MODEL_OPTIONS

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

with st.sidebar:
    model_name = st.selectbox(
        "Select a model",
        options=MODEL_OPTIONS.keys(),
        format_func=lambda x: MODEL_OPTIONS[x].name,
        help="Select the model to use for the chatbot.",
    )
    api_key = MODEL_OPTIONS[model_name].api_key
    f"[Get API key]({MODEL_OPTIONS[model_name].api_key_url})"

st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by Gemini")
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "parts": {"text": "How can I help you?"}}
    ]

if not api_key:
    st.info(f"Please add your {model_name} API key to continue.")
    st.stop()

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["parts"]["text"])

if "gemini-model" not in st.session_state:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name=model_name)
    st.session_state["gemini-model"] = model.start_chat(
        history=st.session_state.messages
    )

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "parts": {"text": prompt}})
    st.chat_message("user").write(prompt)
    response = st.session_state["gemini-model"].send_message(prompt)
    msg = response.text
    st.session_state.messages.append({"role": "assistant", "parts": {"text": msg}})
    st.chat_message("assistant").write(msg)
    print(st.session_state["gemini-model"].history)
