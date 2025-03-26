from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/stock_db")
db = client["stock_db"]
portfolios_collection = db["portfolio"]

class Portfolio:
    def __init__(self, email, symbol, quantity, purchase_price):
        self.email = email
        self.symbol = symbol
        self.quantity = quantity
        self.purchase_price = purchase_price

    def save(self):
        # Save to MongoDB
        portfolios_collection.insert_one({
            "email": self.email,
            "symbol": self.symbol,
            "quantity": self.quantity,
            "purchase_price": self.purchase_price
        })
