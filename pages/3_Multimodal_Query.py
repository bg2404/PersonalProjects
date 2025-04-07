import base64

import streamlit as st
from openai import APIError, BadRequestError, NotFoundError, RateLimitError

try:
    from models.llm import TEXT_MODEL_OPTIONS
    from widgets.sidebar import setup_sidebar
except ImportError as e:
    st.error(f"Failed to import project modules: {e}")
    st.stop()

st.set_page_config(page_title="Multimodal Query", page_icon="🖼️")

try:
    selected_model_name, client = setup_sidebar(TEXT_MODEL_OPTIONS)
    if client is None:
        st.error("Failed to retrieve API client from sidebar setup.")
        st.stop()
except Exception as e:
    st.error("An error occurred during sidebar setup.")
    st.exception(e)
    st.stop()

st.title("🖼️ Multimodal Query")
st.caption(f"🚀 Ask questions with text and optionally an image, powered by {selected_model_name}")

st.divider()

st.write("### Inputs")
text_prompt = st.text_area("Enter text prompt:", height=100)
uploaded_file = st.file_uploader("Upload an image (optional)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.write("Uploaded Image Preview:")
    st.image(uploaded_file, width=300)

st.divider()

if st.button("Submit Query"):
    if client is None:
        st.error("API Client not available. Please check configuration.")
        st.stop()

    if not text_prompt and not uploaded_file:
        st.warning("Please enter a text prompt or upload an image.")
    else:
        content_payload = []
        if text_prompt:
            content_payload.append({"type": "text", "text": text_prompt})

        if uploaded_file:
            try:
                image_bytes = uploaded_file.getvalue()
                image_base64 = base64.b64encode(image_bytes).decode("utf-8")
                # Determine mime type (basic example, relying on browser info)
                mime_type = uploaded_file.type or "image/jpeg"  # Default if type unknown
                content_payload.append(
                    {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{image_base64}"}}
                )
            except Exception as e:
                st.error(f"Error processing uploaded image: {e}")
                st.stop()

        if content_payload:
            st.write("### Response")
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
                    st.markdown(model_response_content)

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
                    # traceback.print_exc() # For debugging in console if needed
