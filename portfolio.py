from flask import Flask, jsonify, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)

# MongoDB Connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/customer_segmentation"
mongo = PyMongo(app)

@app.route('/portfolio', methods=['GET'])
def get_portfolio():
    portfolio_data = mongo.db.portfolio.find_one({}, {"_id": 0})  # Fetch portfolio without _id
    if not portfolio_data:
        return jsonify({"error": "No portfolio found"}), 404
    return jsonify(portfolio_data)

@app.route('/portfolio-page')
def portfolio_page():
    return render_template('portfolio.html')  # Frontend page for portfolio

if __name__ == '__main__':
    app.run(debug=True)
