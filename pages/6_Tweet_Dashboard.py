import pandas as pd
import streamlit as st

from utils.db_handler import DatabaseHandler

st.set_page_config(page_title="Tweet Dashboard", page_icon="📊")

st.title("📊 Tweet Dashboard")
st.caption("View and manage generated tweets.")

db_handler = DatabaseHandler()

# Fetch all tweets from the database
tweets = db_handler.get_all_tweets()

if tweets:
    # Convert the list of Tweet objects to a list of dictionaries
    tweet_list = []
    for tweet in tweets:
        tweet_list.append(
            {
                "ID": tweet.id,
                "Model": tweet.model_name,
                "Personality": tweet.personality,
                "Content Type": tweet.content_type,
                "Content Format": tweet.content_format,
                "Tweet Text": tweet.tweet_text,
                "Posted URL": tweet.posted_url,
                "Created At": tweet.created_at,
            }
        )

    # Convert the list of dictionaries to a Pandas DataFrame
    df = pd.DataFrame(tweet_list)

    # Display the DataFrame in Streamlit
    st.dataframe(df, use_container_width=True)
else:
    st.write("No tweets found in the database.")
