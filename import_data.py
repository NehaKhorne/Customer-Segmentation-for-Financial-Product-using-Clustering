import json
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["stock_db"]
collection = db["users"]

# Load your JSON file
with open("users_portfolio.json", "r") as file:
    data = json.load(file)

# Insert data into MongoDB
collection.insert_many(data)

print("Data imported successfully!")
