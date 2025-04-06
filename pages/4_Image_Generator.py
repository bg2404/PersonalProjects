import streamlit as st
from openai import RateLimitError, APIError, BadRequestError, APIConnectionError, AuthenticationError
import traceback
import base64

try:
    from models.llm import IMAGE_MODEL_OPTIONS
    from widgets.sidebar import setup_sidebar
except ImportError as e:
    st.error(f"Failed to import project modules: {e}")
    st.stop()

st.set_page_config(page_title="Image Generator", page_icon="🎨")

try:
    selected_model_name, client = setup_sidebar(IMAGE_MODEL_OPTIONS)
    if client is None:
        st.error("Failed to retrieve API client from sidebar setup.")
        st.stop()
except Exception as e:
    st.error("An error occurred during sidebar setup.")
    st.exception(e)
    st.stop()

st.title("🎨 Image Generator")
st.caption(f"🚀 Generate images using {selected_model_name}")

st.divider()

st.write("### Image Generation Inputs")
prompt = st.text_area("Enter a prompt for the image:", "A watercolor painting of a futuristic city skyline at sunset")

size_options = ["1024x1024", "1792x1024", "1024x1792"]
selected_size = st.selectbox("Select image size:", size_options, index=0)

st.divider()

if st.button("Generate Image"):
    if client is None:
        st.error("API Client not available. Please check configuration.")
        st.stop()

    if not prompt:
        st.warning("Please enter a prompt for the image.")
    else:
        st.write("### Generated Image")
        with st.spinner("Generating image... Please wait."):
            try:
                # Always request b64_json format for consistency and easier handling in Streamlit
                response_format = "b64_json"

                response = client.images.generate(
                    model=selected_model_name,
                    prompt=prompt,
                    n=1,
                    size=selected_size,
                    response_format=response_format,
                )

                if response.data and len(response.data) > 0 and response.data[0].b64_json:
                    b64_data = response.data[0].b64_json
                    try:
                        image_bytes = base64.b64decode(b64_data)
                        st.image(image_bytes, caption=f"Generated image for: '{prompt}'", use_container_width=True)
                        st.download_button(
                            label="Download Image",
                            data=image_bytes,
                            file_name=f"{prompt[:30].replace(' ','_')}.png",
                            mime="image/png"
                        )
                    except Exception as decode_error:
                        st.error(f"Error decoding base64 image data: {decode_error}")
                else:
                    st.error("API response did not contain expected b64_json data.")
                    st.json(response.model_dump())

            except APIConnectionError as e:
                st.error(f"API Connection Error: {e}")
            except AuthenticationError as e:
                st.error(f"API Authentication Error: Check API Key. {e}")
            except RateLimitError as e:
                st.error(f"API Rate Limit Error: {e}")
            except BadRequestError as e:
                 st.error(f"API Request Error: {e}")
            except APIError as e:
                st.error(f"API Error: Status {e.status_code}. {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred during the API call: {e}")
                # traceback.print_exc() # For debugging in console if needed
