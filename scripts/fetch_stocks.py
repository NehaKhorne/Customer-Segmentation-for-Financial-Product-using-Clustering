import time
from flask import render_template
import yfinance as yf
from pymongo import MongoClient
import datetime

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Ensure MongoDB is running
db = client["stock_database"]
stocks_collection = db["stocks"]

def fetch_stock_data(socketio):
    stock_symbols = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'ICICIBANK.NS',"TATAMOTORS.NS", "WIPRO.NS","TATASTEEL.NS"]
    stock_data = []
    
    for symbol in stock_symbols:
        stock = yf.Ticker(symbol)
        hist = stock.history(period='1d')

        if not hist.empty:
            last_row = hist.iloc[-1]
            stock_info = {
                "symbol": symbol,
                "price": last_row["Close"],
                "high": last_row["High"],
                "low": last_row["Low"],
                "volume": last_row["Volume"]
            }
            stock_data.append(stock_info)
    
    print("Fetched Stock Data:", stock_data)  # Debugging

    return render_template('market_data.html', stocks=stock_data)
