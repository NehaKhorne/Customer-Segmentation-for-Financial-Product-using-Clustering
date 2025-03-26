import yfinance as yf
import pandas as pd

def get_stock_data(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period="1d")
    return {
        "symbol": symbol,
        "price": data['Close'].iloc[-1],
        "volume": data['Volume'].iloc[-1]
    }
