from sqlalchemy import Column, String, Integer, DateTime ,Float ,Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class NewsArticle(Base):
    __tablename__ = 'news_articles'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    summary = Column(Text)
    link = Column(String(255))
    timestamp = Column(DateTime)
    sentiment_score = Column(Float)

    def __repr__(self):
        return f"<NewsArticle(title={self.title}, timestamp={self.timestamp})>"
