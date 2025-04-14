import requests
import os
from dotenv import load_dotenv
from ratelimit import limits, sleep_and_retry

load_dotenv()

@sleep_and_retry
@limits(calls=60, period=60)
def call_api(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("API response: {}".format(response.status_code))
    return response.json()

def fetch_news():
    api_key = os.getenv("API_KEY")
    url = f"https://newsapi.org/v2/everything?q=finance&apiKey={api_key}"

    response = call_api(url)
    data = response

    articles = []

    for article in data['articles']:
        articles.append({
            'title': article['title'],
            'summary': article['description'],
            'link': article['url'],
            'timestamp': article['publishedAt']
        })

    return articles

