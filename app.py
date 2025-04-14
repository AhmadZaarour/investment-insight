from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.news_article import NewsArticle
import json
import os
from dotenv import load_dotenv
from collections import defaultdict
from models.fetch_stock import fetch_stock_data

load_dotenv()

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def dashboard():

    if request.args.get('ticker') and request.args.get('nb_days'):
        ticker = request.args.get('ticker').upper()
        nb_days = request.args.get('nb_days')
    else:
        ticker = 'TSLA'
        nb_days = '5'
    
    if request.args.get('company'):
        company = request.args.get('company')
    else:
        company = "tesla"

    # Fetch news matching the ticker
    articles = session.query(NewsArticle).filter(
        (NewsArticle.title.ilike(f"%{company}%")) |
        (NewsArticle.summary.ilike(f"%{company}%"))
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

    # stock data for plotting

    stock_data = fetch_stock_data(ticker=ticker, period=f"{nb_days}d")
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

    return render_template(
            'dashboard.html', articles=articles,
            sentiment_counts=json.dumps(sentiment_trend),
            ticker=ticker,
            company=company,
            last_price=last_price,
            history=json.dumps(history)
        )

if __name__ == "__main__":
    app.run(debug=True)
