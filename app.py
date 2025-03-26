import eventlet
eventlet.monkey_patch()
import csv
from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_socketio import SocketIO
import threading
import time
import yfinance as yf
from pymongo import MongoClient
import pandas as pd
import os
from bson import ObjectId
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import random


# ✅ Flask setup
app = Flask(__name__)
app.secret_key = "your_secret_key"
socketio = SocketIO(app, cors_allowed_origins="*")

# ✅ MongoDB setup
client = MongoClient("mongodb://localhost:27017/stock_db")
db = client["stock_db"]
portfolios_collection = db["portfolio"]
stocks_collection = db["stocks"]
users_collection = db["users"]

# ✅ Cache for stock prices
stock_cache = {}

# ✅ Load CSV once on startup
csv_path = os.path.join(os.getcwd(), 'scripts', 'static', 'data', 'user_portfolio_sample.csv')
df = pd.read_csv(csv_path)

# ✅ Serialize MongoDB documents
def serialize_document(doc):
    """ Convert MongoDB ObjectId and datetime to serializable format """
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            doc[key] = str(value)
        elif isinstance(value, datetime):
            doc[key] = value.isoformat()
    return doc

# 🚀 Efficient function to fetch stock prices
def fetch_live_prices():
    """Fetch live prices periodically and cache them."""
    global stock_cache
    stock_symbols = df['symbol'].unique().tolist()

    while True:
        for symbol in stock_symbols:
            try:
                stock = yf.Ticker(symbol)
                price = stock.history(period="1d")['Close'].iloc[-1]
                stock_cache[symbol] = price
            except Exception as e:
                print(f"Error fetching {symbol}: {e}")
                stock_cache[symbol] = 0  # Default to 0 if fetch fails

        print("✅ Cached stock prices:", stock_cache)
        time.sleep(30)  # Update every 30 seconds

# ✅ Optimized portfolio calculation
def calculate_portfolio():
    customer_portfolio = []

    for _, row in df.iterrows():
        live_price = stock_cache.get(row['symbol'], row['purchase_price'])

        current_value = live_price * row['quantity']
        purchase_value = row['purchase_price'] * row['quantity']
        profit_loss = current_value - purchase_value

        customer_portfolio.append({
            "name": row['name'],
            "email": row['email'],
            "symbol": row['symbol'],
            "quantity": row['quantity'],
            "purchase_price": row['purchase_price'],
            "current_price": live_price,
            "portfolio_value": current_value,
            "profit_loss": profit_loss
        })

    portfolio_df = pd.DataFrame(customer_portfolio)

    total_value = portfolio_df['portfolio_value'].sum()
    total_profit_loss = portfolio_df['profit_loss'].sum()
    top5 = portfolio_df.nlargest(5, 'profit_loss').to_dict(orient='records')
    worst5 = portfolio_df.nsmallest(5, 'profit_loss').to_dict(orient='records')

    return total_value, total_profit_loss, top5, worst5


# ✅ Real-time stock price socket event
@socketio.on('connect')
def handle_connect():
    print('Client connected')


@socketio.on('portfolio_update')
def send_portfolio_update():
    """Emit portfolio updates to all connected clients."""
    with app.app_context():
        total_value, total_profit_loss, top5, worst5 = calculate_portfolio()

        socketio.emit('portfolio_data', {
            'total_value': total_value,
            'total_profit_loss': total_profit_loss,
            'top5': top5,
            'worst5': worst5
        })


# ✅ Portfolio route
@app.route('/portfolio', methods=['GET'])
def portfolio():
    total_value, total_profit_loss, top5, worst5 = calculate_portfolio()

    return render_template('portfolio.html',
                           total_value=total_value,
                           total_profit_loss=total_profit_loss,
                           top5=top5,
                           worst5=worst5,
                           abs=abs)


# ✅ Dashboard Routes
@app.route('/')
def index():
    return redirect(url_for('home'))


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/home')
def home():
    return render_template('home.html')


def fetch_stock_data(symbol):
    """Fetch stock data using Yahoo Finance."""
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")

        if not data.empty:
            return {
                'symbol': symbol,
                'price': data['Close'].iloc[-1],
                'volume': data['Volume'].iloc[-1],
                'change': data['Close'].iloc[-1] - data['Open'].iloc[-1],
                'high': data['High'].iloc[-1] if 'High' in data else 0,
                'low': data['Low'].iloc[-1] if 'Low' in data else 0
            }
        else:
            # Return default values if no data available
            return {
                'symbol': symbol,
                'price': 0,
                'volume': 0,
                'change': 0,
                'high': 0,
                'low': 0
            }
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return {
            'symbol': symbol,
            'price': 0,
            'volume': 0,
            'change': 0,
            'high': 0,
            'low': 0
        }

# ✅ Market Data with Multi-threading
@app.route('/market_data')
def market_data():
    stock_symbols = [
        "MRF.NS", "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS",
        "ICICIBANK.NS", "KOTAKBANK.NS", "AXISBANK.NS", "ITC.NS",
        "HINDUNILVR.NS", "SBIN.NS", "LT.NS", "BAJFINANCE.NS",
        "MARUTI.NS", "TITAN.NS", "ASIANPAINT.NS", "HCLTECH.NS",
        "WIPRO.NS", "SUNPHARMA.NS", "ULTRACEMCO.NS", "POWERGRID.NS","ZOMATO.NS","SWIGGY.NS", "NESTLEIND.NS", "BRITANNIA.NS", "IDFCFIRSTB.NS", "YESBANK.NS"
    ]

    stock_data = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(fetch_stock_data, symbol): symbol for symbol in stock_symbols}

        for future in as_completed(futures):
            result = future.result()
            if result:
                stock_data.append(result)

    return render_template('market_data.html', stocks=stock_data)


# Function to get real-time stock prices
# 📌 Function to fetch live stock prices
def get_live_price(symbol):
    """Fetch live stock price using yfinance"""
    try:
        stock = yf.Ticker(symbol)
        return round(stock.history(period='1d')['Close'].iloc[-1], 2)
    except Exception as e:
        print(f"Error fetching price for {symbol}: {e}")
        return 0.0

# 📌 Route to get detailed cluster info with real-time pricing
@app.route('/get-cluster-details/<risk_level>')
def get_cluster_details(risk_level):
    cluster_data = users_collection.find({'investment_risk': risk_level})

    results = []
    for customer in cluster_data:
        symbol = customer.get('symbol', '')
        quantity = customer.get('quantity', 0)
        live_price = get_live_price(symbol)
        portfolio_value = live_price * quantity

        results.append({
            'name': customer.get('name', ''),
            'email': customer.get('email', ''),
            'symbol': symbol,
            'quantity': quantity,
            'current_price': live_price,
            'portfolio_value': portfolio_value
        })

    return jsonify(results)


# ✅ New Route to Serve Cluster Data as JSON for Charts
@app.route('/api/clusters')
def api_clusters():
    """Serve cluster data as JSON for chart updates"""
    users = list(users_collection.find({}))
    clusters = {}

    for user in users:
        user = serialize_document(user)
        risk_level = user.get('investment_risk', 'N/A')

        if risk_level not in clusters:
            clusters[risk_level] = {
                'num_customers': 0,
                'total_portfolio_value': 0.0
            }

        symbol = user.get('symbol', '')
        quantity = user.get('quantity', 0)
        current_price = get_live_price(symbol)
        portfolio_value = quantity * current_price

        clusters[risk_level]['num_customers'] += 1
        clusters[risk_level]['total_portfolio_value'] += portfolio_value

    cluster_data = []
    for risk, data in clusters.items():
        cluster_data.append({
            'name': risk,
            'num_customers': data['num_customers'],
            'total_portfolio_value': data['total_portfolio_value']
        })

    return jsonify(cluster_data)


# ✅ Updated clustering route to render HTML (no JSON response here)
@app.route('/clustering')
def clustering():
    """Render the clustering HTML page"""
    users = list(users_collection.find({}))
    clusters = {}

    for user in users:
        user = serialize_document(user)
        risk_level = user.get('investment_risk', 'N/A')

        if risk_level not in clusters:
            clusters[risk_level] = {
                'num_customers': 0,
                'total_portfolio_value': 0.0
            }

        symbol = user.get('symbol', '')
        quantity = user.get('quantity', 0)
        current_price = get_live_price(symbol)
        portfolio_value = quantity * current_price

        clusters[risk_level]['num_customers'] += 1
        clusters[risk_level]['total_portfolio_value'] += portfolio_value

    cluster_data = [
        {
            'name': risk,
            'num_customers': data['num_customers'],
            'avg_portfolio_value': round(data['total_portfolio_value'] / max(data['num_customers'], 1), 2),
            'total_portfolio_value': round(data['total_portfolio_value'], 2)
        }
        for risk, data in clusters.items()
    ]

    return render_template('clustering.html', clusters=cluster_data)


# ✅ Function to fetch all customers (moved from utils.py)
def get_all_customers():
    return list(users_collection.find({}, {"_id": 0}))
# Sample stock data for fallback
stocks_data = [
    {"name": "Reliance Industries", "sector": "Energy", "price": 2450, "change": 1.8, "profitability": 12.5},
    {"name": "Infosys", "sector": "Technology", "price": 1550, "change": -0.5, "profitability": -2.0},
    {"name": "HDFC Bank", "sector": "Finance", "price": 1500, "change": 2.3, "profitability": 8.7},
    {"name": "Tata Steel", "sector": "Metals", "price": 900, "change": -1.2, "profitability": -3.5},
    {"name": "Wipro", "sector": "Technology", "price": 430, "change": 0.9, "profitability": 5.3},
    {"name": "ICICI Bank", "sector": "Finance", "price": 980, "change": 1.7, "profitability": 7.5},
    {"name": "Tata Motors", "sector": "Automobile", "price": 660, "change": -0.8, "profitability": -1.5},
    {"name": "Bharti Airtel", "sector": "Telecom", "price": 850, "change": 2.5, "profitability": 9.2},
    {"name": "Larsen & Toubro", "sector": "Construction", "price": 3000, "change": 1.3, "profitability": 6.8},
    {"name": "HUL", "sector": "Consumer Goods", "price": 2700, "change": -1.0, "profitability": -2.1},
    {"name": "Adani Ports", "sector": "Infrastructure", "price": 1400, "change": 3.2, "profitability": 11.0},
    {"name": "Tech Mahindra", "sector": "Technology", "price": 1350, "change": -0.4, "profitability": -0.9},
]

# ✅ Fetch real-time stock price and change
def fetch_realtime_stock_data(symbol):
    """Fetch real-time price and change for a given stock symbol."""
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")

        if not data.empty:
            latest_price = data['Close'].iloc[-1]
            previous_close = data['Close'].iloc[-2] if len(data) > 1 else latest_price
            change = ((latest_price - previous_close) / previous_close) * 100
            return latest_price, round(change, 2)
        else:
            return random.randint(100, 3000), random.uniform(-5, 5)

    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return random.randint(100, 3000), random.uniform(-5, 5)


# ✅ Generate a reason for the recommendation
def generate_reason(customer, stock):
    reasons = []

    # Income-based reasoning
    if customer['annual_income'] > 1000000 and stock['price'] > 2000:
        reasons.append("High-value stock suitable for high-income investors.")
    elif customer['annual_income'] <= 1000000 and stock['price'] < 1500:
        reasons.append("Affordable stock suitable for moderate-income investors.")
    
    # Risk-based reasoning
    if customer['investment_risk'].lower() == 'low' and stock['change'] > 0:
        reasons.append("Low-risk investment with stable growth potential.")
    elif customer['investment_risk'].lower() == 'high' and stock['change'] < 0:
        reasons.append("High-risk stock with potential for high returns.")
    
    # Sector preference reasoning
    if stock['sector'].lower() == customer['preferred_sector'].lower():
        reasons.append(f"Matches your sector preference: {customer['preferred_sector']}.")
    
    return " ".join(reasons) if reasons else "Diversified stock recommendation."


# ✅ Route to display real-time stock recommendations
@app.route('/recommendations')
def recommendations():
    customers_df = pd.read_csv(csv_path)

    recommendations = []

    for _, row in customers_df.iterrows():
        customer = {
            "name": row['name'],
            "email": row['email'],
            "annual_income": row['annual_income'],
            "investment_risk": row['investment_risk'],
            "preferred_sector": row['preferred_sector']
        }

        # Select sector and other stocks
        sector_stocks = [stock for stock in stocks_data if stock['sector'].lower() == customer['preferred_sector'].lower()]
        other_stocks = [stock for stock in stocks_data if stock['sector'].lower() != customer['preferred_sector'].lower()]

        # Combine sector and random stocks
        recommended_stocks = random.sample(sector_stocks, min(3, len(sector_stocks))) + random.sample(other_stocks, 5 - min(3, len(sector_stocks)))

        # Fetch real-time prices
        stock_recommendations = []
        for stock in recommended_stocks:
            # Map stock names to symbols for real-time fetching
            stock_symbols = {
                "Reliance Industries": "RELIANCE.NS",
                "Infosys": "INFY.NS",
                "HDFC Bank": "HDFCBANK.NS",
                "Tata Steel": "TATASTEEL.NS",
                "Wipro": "WIPRO.NS",
                "ICICI Bank": "ICICIBANK.NS",
                "Tata Motors": "TATAMOTORS.NS",
                "Bharti Airtel": "BHARTIARTL.NS",
                "Larsen & Toubro": "LT.NS",
                "HUL": "HINDUNILVR.NS",
                "Adani Ports": "ADANIPORTS.NS",
                "Tech Mahindra": "TECHM.NS"
            }

            symbol = stock_symbols.get(stock['name'], "RELIANCE.NS")
            price, change = fetch_realtime_stock_data(symbol)

            stock_with_reason = {
                "name": stock['name'],
                "sector": stock['sector'],
                "price": price,
                "change": change,
                "reason": generate_reason(customer, {"price": price, "change": change, "sector": stock['sector']})
            }
            stock_recommendations.append(stock_with_reason)

        recommendations.append({
            "customer": customer,
            "stocks": stock_recommendations
        })

    return render_template('recommendations.html', recommendations=recommendations)


# Route to calculate SIP
@app.route('/calculate_sip', methods=['POST'])
def calculate_sip():
    try:
        monthly_investment = float(request.form['monthly_investment'])
        return_rate = float(request.form['return_rate']) / 100
        time_period = int(request.form['time_period'])

        # SIP formula calculation
        n = 12  # Compounded monthly
        invested_amount = monthly_investment * time_period * n

        # Future value formula
        fv = monthly_investment * (((1 + return_rate / n)**(n * time_period) - 1) / (return_rate / n)) * (1 + return_rate / n)

        estimated_returns = fv - invested_amount
        total_value = fv

        # Return the results as JSON
        return jsonify({
            'invested_amount': f"₹{invested_amount:,.2f}",
            'estimated_returns': f"₹{estimated_returns:,.2f}",
            'total_value': f"₹{total_value:,.2f}"
        })

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/watchlist')
def watchlist():
    return render_template('watchlist.html')


# ✅ Start the server
if __name__ == '__main__':
    price_thread = threading.Thread(target=fetch_live_prices, daemon=True)
    price_thread.start()

    # Use only one socketio.run()
    socketio.run(app, host='0.0.0.0', port=10000, allow_unsafe_werkzeug=True, debug=True)

