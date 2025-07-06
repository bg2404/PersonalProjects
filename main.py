import streamlit as st

st.set_page_config(
    page_title="Streamlit App Hub",
    page_icon="🚀",
    layout="wide",  # Use "wide" layout for better spacing of columns
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
col5, col6 = st.columns(2)
col7, col8 = st.columns(2)
col9, col10 = st.columns(2)

with col1:
    st.subheader("🏠 Mortgage Calculator")
    st.markdown("Calculate monthly mortgage payments based on loan amount, interest rate, and term.")
    # Use st.page_link for internal navigation (Streamlit 1.33+)
    if hasattr(st, "page_link"):
        st.page_link("pages/1_Mortgage_Calculator.py", label="Go to Calculator", icon="🏠")
    else:
        # Fallback for older Streamlit versions assumes page filename is the URL path
        st.markdown("[Go to Calculator](1_Mortgage_Calculator)")

with col2:
    st.subheader("💬 Chatbot")
    st.markdown("Interact with different AI chat models.")
    if hasattr(st, "page_link"):
        st.page_link("pages/2_Chatbot.py", label="Start Chatting", icon="💬")
    else:
        st.markdown("[Start Chatting](2_Chatbot)")

with col3:
    st.subheader("🖼️ Multimodal Query")
    st.markdown("Ask questions using text and an optional uploaded image.")
    # Ensure the link points to the correct file name if you renamed it
    if hasattr(st, "page_link"):
        st.page_link("pages/3_Multimodal_Query.py", label="Ask with Image", icon="🖼️")
    else:
        # Update link text if file renamed
        st.markdown("[Ask with Image](3_Multimodal_Query)")

with col4:
    st.subheader("🎨 Image Generator")
    st.markdown("Generate images from text prompts using AI models.")
    if hasattr(st, "page_link"):
        st.page_link("pages/4_Image_Generator.py", label="Generate Image", icon="🎨")
    else:
        st.markdown("[Generate Image](4_Image_Generator)")

with col5:
    st.subheader("📲 Tweet Generator")
    st.markdown("Generate tweets based on selected personality and content type.")
    if hasattr(st, "page_link"):
        st.page_link("pages/5_Tweet_Generator.py", label="Generate Tweet", icon="📲")
    else:
        st.markdown("[Generate Tweet](5_Tweet_Generator)")

with col6:
    st.subheader("📊 Tweet Dashboard")
    st.markdown("View and manage generated tweets.")
    if hasattr(st, "page_link"):
        st.page_link("pages/6_Tweet_Dashboard.py", label="View Dashboard", icon="📊")
    else:
        st.markdown("[View Dashboard](6_Tweet_Dashboard)")

with col7:
    st.subheader("📈 News Retriever")
    st.markdown("Enter a topic to get the latest news.")
    if hasattr(st, "page_link"):
        st.page_link("pages/7_News_Retriever.py", label="Get News", icon="📈")
    else:
        st.markdown("[Get News](7_News_Retriever)")

with col8:
    st.subheader("📰 Article Generator")
    st.markdown("Generate Articles.")
    if hasattr(st, "page_link"):
        st.page_link("pages/8_Article_Generator.py", label="Generate Article", icon="📰")
    else:
        st.markdown("[Generate Article](8_Article_Generator)")

with col9:
    st.subheader("📰 Finshots Scraper")
    st.markdown("Scrape articles from Finshots.")
    if hasattr(st, "page_link"):
        st.page_link("pages/9_Finshots_scraper.py", label="Scrape Articles", icon="📰")
    else:
        st.markdown("[Scrape Articles](9_Finshots_scraper)")

with col10:
    st.subheader("📈 Index Creator")
    st.markdown("Create an index for top 100 US stocks by market cap.")
    if hasattr(st, "page_link"):
        st.page_link("pages/10_Index_Creator.py", label="Create Index", icon="📈")
    else:
        st.markdown("[Create Index](10_Index_Creator)")

st.divider()

with st.expander("About this Project"):
    st.markdown("""
        * **Goal:** Learn Streamlit and explore different app types (calculations, AI, image handling).
        * **Technologies:** Python, Streamlit, AI APIs.
        * **Status:** Work in progress!
    """)
