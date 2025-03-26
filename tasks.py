from celery import Celery
import yfinance as yf
from pymongo import MongoClient

# Initialize Celery
app = Celery("tasks", broker="redis://localhost:6379/0")

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["stock_market"]
collection = db["stocks"]

@app.task
def update_stock_data(symbol="RELIANCE.NS"):
    stock = yf.Ticker(symbol)
    data = stock.history(period="1d")

    if not data.empty:
        stock_data = {
            "symbol": symbol,
            "price": round(data["Close"].iloc[-1], 2),
            "volume": int(data["Volume"].iloc[-1])
        }
        collection.update_one({"symbol": symbol}, {"$set": stock_data}, upsert=True)
        print(f"Updated {symbol}: ₹{stock_data['price']}")

def start_celery_tasks():
    app.send_task("tasks.update_stock_data", args=["RELIANCE.NS"], countdown=10)
