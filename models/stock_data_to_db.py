from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import datetime
import os
from dotenv import load_dotenv
from ML import analyze_news_sentiment as ans
from dbTables import stock_news as sn

load_dotenv()

# DB setup
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
sn.Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def save_stock_news_to_db(news):
    for article in news:
        stock_news = sn.StockNews(
            ticker=article['ticker'],
            company=article['company'],
            title=article['title'],
            summary=article['summary'],
            timestamp=datetime.datetime.fromisoformat(article['timestamp']),
            sentiment_score = article['sentiment_score']
        )

        try:
            session.add(stock_news)
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
    
    ticker = 'GOOG'
    articles = ans.fetch_and_analyze_stock_news(ticker)
    if articles:
        save_stock_news_to_db(articles)
        print(f"Successfully saved {len(articles)} articles with sentiment scores to MySQL.")
    else:
        print("No articles were saved.")