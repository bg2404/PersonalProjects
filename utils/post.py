import tweepy

from utils.api import X_API


def post_to_x(content):
    client = tweepy.Client(
        consumer_key=X_API.get("api_key"),
        consumer_secret=X_API.get("api_key_secret"),
        access_token=X_API.get("access_token"),
        access_token_secret=X_API.get("access_token_secret"),
    )

    try:
        response = client.create_tweet(text=content)
        if X_API.get("username") is None:
            return True
        return f"https://x.com/{X_API.get('username')}/status/{response.data['id']}"
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
