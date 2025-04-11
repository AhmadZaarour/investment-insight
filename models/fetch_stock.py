import yfinance as yf

def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    
    # Get latest price
    stock_info = stock.info
    latest_price = stock_info.get("regularMarketPrice", None)

    # Get historical data (last 5 days)
    hist = stock.history(period="5d")

    return {
        "ticker": ticker,
        "latest_price": latest_price,
        "history": hist.reset_index()[["Date", "Close"]].to_dict(orient="records")
    }
