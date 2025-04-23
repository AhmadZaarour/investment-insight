from sqlalchemy.orm import sessionmaker
from dbTables.news_article import NewsArticle, Base
from sqlalchemy import create_engine
import datetime
import os
from dotenv import load_dotenv
from ML.analyze_news_sentiment import fetch_and_analyze_news

load_dotenv()

# DB setup
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def save_articles_to_db(articles):
    for article in articles:
        news_article = NewsArticle(
            title=article['title'],
            summary=article['summary'],
            link=article['link'],
            timestamp=datetime.datetime.fromisoformat(article['timestamp']),
            sentiment_score = article['sentiment_score']
        )
        try:
            session.add(news_article)
        except:
            session.rollback()
            raise
    try:
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    
    articles = fetch_and_analyze_news()
    if articles:
        save_articles_to_db(articles)
        print(f"Successfully saved {len(articles)} articles with sentiment scores to MySQL.")
    else:
        print("No articles were saved.")
