import yfinance as yf
from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter
class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
   pass

def fetch_stock_data(ticker, period):

    session = CachedLimiterSession(
        limiter=Limiter(RequestRate(2, Duration.SECOND*5)),  # max 2 requests per 5 seconds
        bucket_class=MemoryQueueBucket,
        backend=SQLiteCache("yfinance.cache"),
    )
    # Get latest price
    stock = yf.Ticker(ticker, session=session)
    stock_info = stock.info
    latest_price = stock_info.get("regularMarketPrice", None)

    # Get historical data
    hist = stock.history(period)

    return {
        "ticker": ticker,
        "latest_price": latest_price,
        "history": hist.reset_index()[["Date", "Close"]].to_dict(orient="records")
    }