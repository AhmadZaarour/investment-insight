from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.dbTables.news_article import NewsArticle
from models.dbTables.stock_news import StockNews
import json
import os
from dotenv import load_dotenv
from collections import defaultdict
from models.fetching.fetch_stock import fetch_stock_data

load_dotenv()

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def fetch_and_plot(news, company):
    try:
        # Fetch news matching the ticker from db
        articles = session.query(news).filter(
            (news.title.ilike(f"%{company}%")) |
            (news.summary.ilike(f"%{company}%"))
        ).all()

        # sentiment score trends for plotting
        daily_scores = defaultdict(list)
        for article in articles:
            if article.timestamp:
                date_str = article.timestamp.strftime('%Y-%m-%d')
                daily_scores[date_str].append(article.sentiment_score)

        daily_avg_sentiment = {
            date: sum(scores) / len(scores)
            for date, scores in daily_scores.items()
        }

        sorted_dates = sorted(daily_avg_sentiment.keys())
        sentiment_trend = {
            'dates': sorted_dates,
            'scores': [daily_avg_sentiment[date] for date in sorted_dates]
        }
    except:
        session.rollback()
        raise
    finally:
        session.close()

        return articles, sentiment_trend

@app.route('/')
def dashboard():

    if request.args.get('ticker') and request.args.get('nb_days') and request.args.get('period'):
        ticker = request.args.get('ticker').upper()
        nb_days = f"{request.args.get('nb_days')}{request.args.get('period')}"
        stock_articles, stock_sentiment_trend = fetch_and_plot(StockNews, ticker)  # Fetch stock news articles and sentiment trend

        stock_data = fetch_stock_data(ticker=ticker, period=f"{nb_days}")
        if not stock_data:
            return render_template('error.html', message="Stock data not found.")

        ticker = stock_data['ticker']
        last_price = stock_data['latest_price']
        history_data = stock_data['history']
        
        history_list = defaultdict(list)
        for item in history_data:
            date_str = item["Date"].strftime('%Y-%m-%d')
            history_list[date_str].append(item["Close"])

        history_dict = {
            date: close
            for date, close in history_list.items()
        }


        sorted_dates = sorted(history_dict.keys())
        history = {
            'dates': sorted_dates,
            'close': [(history_dict[date]) for date in sorted_dates]
        }

    else:
        ticker = ''
        stock_articles = []
        stock_sentiment_trend = {}
        last_price = None
        history = {}
    
    if request.args.get('company'):
        company = request.args.get('company')
        articles, sentiment_trend = fetch_and_plot(NewsArticle, company)  # Fetch news articles and sentiment trend

    else:
        company = ""
        articles = []
        sentiment_trend = {}

    return render_template(
            'dashboard.html', articles=articles, stock_articles=stock_articles,
            sentiment_counts=json.dumps(sentiment_trend),
            stock_sentiment_counts=json.dumps(stock_sentiment_trend),
            ticker=ticker,
            company=company,
            last_price=last_price,
            history=json.dumps(history)
        )

if __name__ == "__main__":
    app.run(debug=True)
