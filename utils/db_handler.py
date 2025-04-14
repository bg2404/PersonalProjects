from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.tweet import Base, Tweet


class DatabaseHandler:
    """
    Handles database interactions for storing generated tweets.
    """

    def __init__(self, db_url="sqlite:///tweets.db"):
        """
        Initializes the database connection.

        Args:
            db_url (str): The database URL. Defaults to SQLite.
        """
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_tweet(self, model_name, personality, content_type, content_format, tweet_text, posted_url=None):
        """
        Adds a tweet to the database.

        Args:
            model_name (str): The name of the model used to generate the tweet.
            personality (str): The personality used for tweet generation.
            content_type (str): The content type of the tweet.
            content_format (str): The format of the tweet.
            tweet_text (str): The generated tweet text.
            posted_url (str, optional): The URL where the tweet was posted. Defaults to None.
        """
        session = self.Session()
        try:
            new_tweet = Tweet(
                model_name=model_name,
                personality=personality,
                content_type=content_type,
                content_format=content_format,
                tweet_text=tweet_text,
                posted_url=posted_url,
            )
            session.add(new_tweet)
            session.commit()
            print(f"Tweet saved to database with id {new_tweet.id}")
            return new_tweet.id
        except Exception as e:
            session.rollback()
            print(f"Error adding tweet to database: {e}")
            return None
        finally:
            session.close()

    def update_tweet_url(self, tweet_id, posted_url):
        """
        Updates the posted URL for a tweet in the database.

        Args:
            tweet_id (int): The ID of the tweet to update.
            posted_url (str): The URL where the tweet was posted.
        """
        session = self.Session()
        try:
            tweet = session.query(Tweet).filter(Tweet.id == tweet_id).first()
            if tweet:
                tweet.posted_url = posted_url
                session.commit()
                print(f"Tweet {tweet_id} updated with posted_url {posted_url}")
            else:
                print(f"Tweet with id {tweet_id} not found")
        except Exception as e:
            session.rollback()
            print(f"Error updating tweet: {e}")
        finally:
            session.close()

    def get_all_tweets(self):
        """
        Retrieves all tweets from the database.

        Returns:
            list: A list of all tweets.
        """
        session = self.Session()
        try:
            tweets = session.query(Tweet).order_by(Tweet.created_at.desc()).all()
            return tweets
        finally:
            session.close()

    def get_tweet(self, tweet_id):
        """
        Retrieves a tweet from the database by ID.

        Args:
            tweet_id (int): The ID of the tweet to retrieve.

        Returns:
            Tweet: The tweet object, or None if not found.
        """
        session = self.Session()
        try:
            tweet = session.query(Tweet).filter(Tweet.id == tweet_id).first()
            return tweet
        finally:
            session.close()


# Example Usage (for testing)
if __name__ == "__main__":
    db_handler = DatabaseHandler()  # Uses SQLite by default
    # Add a tweet
    tweet_id = db_handler.add_tweet(
        model_name="GPT-4o",
        personality="Enthusiastic Optimist",
        content_type="Informative Snippets and Facts",
        content_format="Text",
        tweet_text="This is a test tweet!",
    )

    if tweet_id:
        # Update the tweet with a posted URL
        db_handler.update_tweet_url(tweet_id, "https://x.com/example/status/12345")

        # Retrieve the tweet
        retrieved_tweet = db_handler.get_tweet(tweet_id)
        print(f"Retrieved tweet: {retrieved_tweet}")
