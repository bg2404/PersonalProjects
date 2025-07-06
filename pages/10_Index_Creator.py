import requests
import streamlit as st

from utils.api_config import POLYGON_API

st.set_page_config(page_title="Index Creator", page_icon="📈")
st.title("📈 Index Creator")
st.write("Create an index for top 100 US stocks by market cap.")

session = requests.Session()
session.headers.update({"authorization": POLYGON_API["key"]})
