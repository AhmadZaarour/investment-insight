from textblob import TextBlob
from fetching import fetch_news
from fetching import fetch_stock

def analyze_sentiment(text):
    # Analyze the sentiment of the text using TextBlob
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity  # Ranges from -1 (negative) to 1 (positive)
    return sentiment

def fetch_and_analyze_news():
    articles = fetch_news.fetch_news()
    for article in articles:
        sentiment_score = analyze_sentiment(article['summary'])
        article['sentiment_score'] = sentiment_score
    print(f"Fetched and analyzed {len(articles)} articles.")
    return articles

def fetch_and_analyze_stock_news(ticker):
    articles = fetch_stock.fetch_stock_news(ticker)
    for article in articles:
        sentiment_score = analyze_sentiment(article['summary'])
        article['sentiment_score'] = sentiment_score
    print(f"Fetched and analyzed {len(articles)} stock news articles.")
    return articles