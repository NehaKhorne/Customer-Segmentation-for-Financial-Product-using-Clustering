import os
import sqlite3

# Ensure the "instances" directory exists
if not os.path.exists("instances"):
    os.makedirs("instances")

# Connect to SQLite database
conn = sqlite3.connect("instances/database.db")
cursor = conn.cursor()

# Create the users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# Create the investments table
cursor.execute("""
CREATE TABLE IF NOT EXISTS investments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    stock_symbol TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    invested_amount REAL NOT NULL,
    current_price REAL,
    FOREIGN KEY (user_id) REFERENCES user (id)
)
""")

conn.commit()
conn.close()

print("✅ Database initialized successfully!")
