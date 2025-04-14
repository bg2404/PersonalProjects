from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Tweet(Base):
    """
    Model for storing generated tweets.
    """

    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True)
    model_name = Column(String)
    personality = Column(String)
    content_type = Column(String)
    content_format = Column(String)
    tweet_text = Column(Text)
    posted_url = Column(String, nullable=True)  # URL if posted successfully
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Tweet(tweet_text='{self.tweet_text[:50]}...', posted_url='{self.posted_url}')>"
