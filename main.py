import streamlit as st

st.set_page_config(
    page_title="Streamlit App Hub",
    page_icon="🚀",
    layout="wide" # Use "wide" layout for better spacing of columns
)

st.title("🚀 Welcome to the Streamlit App Hub!")
st.markdown("""
This is a collection of tools built with Streamlit. Explore the different functionalities using the links below or the sidebar navigation.
This project is a playground for learning and experimenting with Streamlit features.
""")
st.divider()

st.header("Explore the Tools")

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    st.subheader("🏠 Mortgage Calculator")
    st.markdown("Calculate monthly mortgage payments based on loan amount, interest rate, and term.")
    # Use st.page_link for internal navigation (Streamlit 1.33+)
    if hasattr(st, 'page_link'):
        st.page_link("pages/1_Mortgage_Calculator.py", label="Go to Calculator", icon="🏠")
    else:
        # Fallback for older Streamlit versions assumes page filename is the URL path
        st.markdown("[Go to Calculator](1_Mortgage_Calculator)")

with col2:
    st.subheader("💬 Chatbot")
    st.markdown("Interact with different AI chat models.")
    if hasattr(st, 'page_link'):
        st.page_link("pages/2_Chatbot.py", label="Start Chatting", icon="💬")
    else:
        st.markdown("[Start Chatting](2_Chatbot)")

with col3:
    st.subheader("🖼️ Multimodal Query")
    st.markdown("Ask questions using text and an optional uploaded image.")
    # Ensure the link points to the correct file name if you renamed it
    if hasattr(st, 'page_link'):
        st.page_link("pages/3_Multimodal_Query.py", label="Ask with Image", icon="🖼️")
    else:
        # Update link text if file renamed
        st.markdown("[Ask with Image](3_Multimodal_Query)")

with col4:
    st.subheader("🎨 Image Generator")
    st.markdown("Generate images from text prompts using AI models.")
    if hasattr(st, 'page_link'):
        st.page_link("pages/4_Image_Generator.py", label="Generate Image", icon="🎨")
    else:
        st.markdown("[Generate Image](4_Image_Generator)")

st.divider()

with st.expander("About this Project"):
    st.markdown("""
        * **Goal:** Learn Streamlit and explore different app types (calculations, AI, image handling).
        * **Technologies:** Python, Streamlit, AI APIs.
        * **Status:** Work in progress!
    """)
