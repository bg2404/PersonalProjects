import json
import urllib.parse
from urllib.request import Request, urlopen

import streamlit as st

from utils.api_config import NEWS_API


def get_news(query):
    """
    Fetches news articles based on a query using the News API.

    Args:
        query (str): The search query for the news articles.

    Returns:
        dict: A dictionary containing the news articles in JSON format.
              Returns an error message if the API request fails.
    """
    api_key = NEWS_API.get("key")
    if not api_key:
        return {"error": "News API key is missing. Please provide a valid API key."}

    base_url = "https://newsapi.org/v2/everything"
    # URL-encode the query to handle spaces and special characters
    encoded_query = urllib.parse.quote_plus(query)
    url = f"{base_url}?q={encoded_query}&apiKey={api_key}"
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})  # Add user agent to avoid blocking
    try:
        with urlopen(req) as response:
            data = response.read()
            news_json = json.loads(data.decode("utf-8"))
        return news_json
    except Exception as e:
        return {"error": f"Failed to fetch news: {e}"}


def display_news(news_data):
    """
    Displays the news articles in a Streamlit app.

    Args:
        news_data (dict): A dictionary containing the news articles.
    """
    if "error" in news_data:
        st.error(news_data["error"])
        return

    if news_data["status"] == "ok" and news_data["articles"]:
        st.header("Latest News")
        for article in news_data["articles"]:
            st.subheader(article["title"])
            # Use st.markdown to handle HTML in description, and for links
            st.markdown(f"<a href='{article['url']}'>Read more</a>", unsafe_allow_html=True)
            st.write(article["description"])
            st.write(f"Source: {article['source']['name']}")
            st.write(f"Published: {article['publishedAt']}")
            if article["urlToImage"]:  # Check if image URL exists
                st.image(article["urlToImage"], caption=article["title"], use_container_width=True)
            st.markdown("---")  # Add a separator between articles
    elif news_data["status"] == "ok" and not news_data["articles"]:
        st.info("No articles found for the given query.")
    else:
        st.error(f"Error: {news_data['message']}")


st.title("News Generator App")
st.write("Enter a topic to get the latest news.")

# Get user input for the news query
query = st.text_input("Topic:", "World")

if st.button("Get News"):
    with st.spinner("Fetching news..."):
        news_data = get_news(query)
    display_news(news_data)
