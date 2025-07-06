import json

import requests
import streamlit as st
from bs4 import BeautifulSoup

from utils.load_json import load_news_articles


def scrape_finshots(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        title = soup.find("h1", class_="article-title").text.strip()
        content = soup.find("section", class_="gh-content")
        hr_tags = content.find_all("hr")
        if hr_tags:
            last_hr = hr_tags[-1]
            for elem in last_hr.find_next_siblings():
                elem.decompose()
            last_hr.decompose()
        extracted_text = content.get_text(separator="\n", strip=True)
        return {"title": title, "content": str(extracted_text)}

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except AttributeError as e:
        print(f"Attribute error (likely element not found): {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def get_all_articles(archive_url="https://finshots.in/archive/"):
    try:
        response = requests.get(archive_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        for a_tag in soup.find_all("a", class_="post-card-image-link"):
            article_url = a_tag["href"]
            articles.append(article_url)
        return articles
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []


def save_to_json(data, filename="data/news_articles.json"):
    """
    Saves the scraped article to the news_articles.json file under the Finshots persona,
    checking if the article already exists before adding it.

    Args:
        data (dict): A dictionary containing the scraped article's title and content.
        filename (str): The path to the news_articles.json file.
    """
    try:
        news_data = load_news_articles(filename)
        finshots_persona = next((p for p in news_data["personas"] if p["name"] == "Finshots"), None)

        if not finshots_persona:
            print("Finshots persona not found in JSON data.")
            return

        article_exists = any(article["title"] == data["title"] for article in finshots_persona["articles"])

        if not article_exists:
            finshots_persona["articles"].append(data)
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(news_data, file, indent=4, ensure_ascii=False)
            print(f"Article '{data['title']}' added to {filename}")
        else:
            print(f"Article '{data['title']}' already exists in {filename}")

    except FileNotFoundError:
        print(f"File not found: {filename}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {filename}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


st.title("Finshots Article Scraper")

article_url = st.text_input("Enter Finshots Article URL:")

articles = get_all_articles()
st.write(articles)

if st.button("Scrape Article"):
    for article_url in articles:
        url = "https://finshots.in" + article_url
        st.write(url)
        article_data = scrape_finshots(url)

        if article_data:
            st.header(article_data["title"])
            save_to_json(article_data)
            st.success(f"Article '{article_data['title']}' saved successfully!")
        else:
            st.error("Failed to scrape the article. Please check the URL and try again.")
