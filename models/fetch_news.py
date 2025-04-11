import requests
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_news():
    api_key = os.getenv("API_KEY")
    url = f"https://newsapi.org/v2/everything?q=finance&apiKey={api_key}"

    response = requests.get(url)
    data = response.json()

    articles = []

    for article in data['articles']:
        articles.append({
            'title': article['title'],
            'summary': article['description'],
            'link': article['url'],
            'timestamp': article['publishedAt']
        })

    return articles

