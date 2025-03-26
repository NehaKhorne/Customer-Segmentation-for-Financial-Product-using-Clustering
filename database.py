from pymongo import MongoClient
from config import config  # Import config to get MongoDB URI

# Connect to MongoDB
client = MongoClient(config.MONGO_URI)
db = client["customer_segmentation"]  # Database name

# Collections
users_collection = db["users"]
investments_collection = db["investments"]
stocks_collection = db["stocks"]  # Add this for real-time stock data
