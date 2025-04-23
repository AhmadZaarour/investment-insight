from sqlalchemy import Column, String, Integer, DateTime ,Float ,Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class StockNews(Base):

    __tablename__ = 'stock_news_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(10), nullable=False)
    company = Column(String(10), nullable=False)
    title = Column(String(255), nullable=False)
    summary = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    sentiment_score = Column(Float, nullable=True)

    def __repr__(self):
        return f"<NewsArticle(title={self.title}, timestamp={self.timestamp})>"