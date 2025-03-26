import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import os

# Initialize Faker for random names and emails
fake = Faker()

# Sample data options
stock_symbols = ["TCS.NS", "RELIANCE.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS", 
                 "HINDUNILVR.NS", "WIPRO.NS", "BAJFINANCE.NS", "SBIN.NS", "LT.NS"]
risks = ['low', 'medium', 'high']
sectors = ['Finance', 'Tech', 'Healthcare', 'Energy', 'Automobile']

# Generate sample data
num_records = 50  # Number of rows
data = []

for _ in range(num_records):
    name = fake.name()
    email = fake.email()
    password = f"Pass@{random.randint(1000, 9999)}"
    symbol = random.choice(stock_symbols)
    quantity = random.randint(1, 100)
    purchase_price = round(random.uniform(100, 5000), 2)
    
    # Random date in the last 5 years
    start_date = datetime(2020, 1, 1)
    end_date = datetime.today()
    purchase_date = fake.date_between(start_date=start_date, end_date=end_date)
    
    annual_income = random.randint(500000, 2000000)
    investment_risk = random.choice(risks)
    preferred_sector = random.choice(sectors)

    data.append({
        "name": name,
        "email": email,
        "password": password,
        "symbol": symbol,
        "quantity": quantity,
        "purchase_price": purchase_price,
        "purchase_date": purchase_date,
        "annual_income": annual_income,
        "investment_risk": investment_risk,
        "preferred_sector": preferred_sector
    })

# Create DataFrame
df = pd.DataFrame(data)

# Define the folder and filename
csv_folder = "static/data"
csv_filename = "user_portfolio_sample.csv"

# Ensure the folder exists
os.makedirs(csv_folder, exist_ok=True)

# Save to CSV
csv_path = os.path.join(csv_folder, csv_filename)
df.to_csv(csv_path, index=False)

print(f"CSV file saved at: {csv_path}")
