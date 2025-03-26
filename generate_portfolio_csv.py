import pandas as pd
import random
from datetime import datetime, timedelta

# Indian names for variety
indian_names = [
    "Neha Sharma", "Divya Singh", "Abhirami Nair", "Sushmita Roy", "Sonal Mehta",
    "Aarav Kapoor", "Rohan Malhotra", "Ishaan Verma", "Pooja Iyer", "Anjali Desai",
    "Kavya Bansal", "Ritika Joshi", "Varun Choudhary", "Aditya Rao", "Priya Menon",
    "Krishna Reddy", "Rajesh Gupta", "Simran Kaur", "Amit Patel", "Meera Srinivasan"
]

# Random stock symbols (NSE)
stock_symbols = ["TCS.NS", "INFY.NS", "RELIANCE.NS", "HDFCBANK.NS", "WIPRO.NS", 
                 "HINDUNILVR.NS", "ICICIBANK.NS", "LT.NS", "BAJFINANCE.NS", "SBIN.NS"]

# Sectors
sectors = ["Tech", "Finance", "Energy", "Healthcare", "Automobile"]

# Risk profiles
risk_profiles = ["low", "medium", "high"]

# Function to generate a random date within the last 3 years
def random_date():
    start_date = datetime.now() - timedelta(days=3*365)
    random_days = random.randint(0, 3*365)
    return (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d')

# Generate dataset
data = []
num_users = 50  # Number of users

for _ in range(num_users):
    name = random.choice(indian_names)
    email = f"{name.split()[0].lower()}.{random.randint(1, 99)}@gmail.com"
    
    # Plain text password
    password = f"Pass@{random.randint(1000, 9999)}"

    symbol = random.choice(stock_symbols)
    quantity = random.randint(1, 100)
    purchase_price = round(random.uniform(100, 5000), 2)
    
    purchase_date = random_date()
    annual_income = random.randint(500000, 2000000)
    risk = random.choice(risk_profiles)
    sector = random.choice(sectors)

    data.append({
        "name": name,
        "email": email,
        "password": password,
        "symbol": symbol,
        "quantity": quantity,
        "purchase_price": purchase_price,
        "purchase_date": purchase_date,
        "annual_income": annual_income,
        "investment_risk": risk,
        "preferred_sector": sector
    })

# Create a DataFrame
df = pd.DataFrame(data)

# Save to CSV
csv_filename = "user_portfolio_data_plain_password.csv"
df.to_csv(csv_filename, index=False)

print(f"✅ CSV file '{csv_filename}' generated successfully with plain text passwords!")
