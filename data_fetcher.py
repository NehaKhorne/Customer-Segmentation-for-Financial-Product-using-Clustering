import yfinance as yf
from database import stocks_collection

# List of Indian stock symbols (NSE format)
stock_symbols = ["TCS.NS", "INFY.NS", "HDFCBANK.NS", "RELIANCE.NS", "ICICIBANK.NS"]  # Add more

def fetch_stock_data():
    data = []
    for symbol in stock_symbols:
        stock = yf.Ticker(symbol)
        info = stock.history(period="1d")

        if not info.empty:
            latest = info.iloc[-1]
            stock_data = {
                "symbol": symbol,
                "open": latest["Open"],
                "high": latest["High"],
                "low": latest["Low"],
                "close": latest["Close"],
                "volume": latest["Volume"]
            }
            data.append(stock_data)
            stocks_collection.update_one({"symbol": symbol}, {"$set": stock_data}, upsert=True)

    print("✅ Stock data updated successfully!")

if __name__ == "__main__":
    fetch_stock_data()
