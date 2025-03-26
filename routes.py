from flask import Blueprint, jsonify
from database import stocks_collection, users_collection

stock_blueprint = Blueprint("stock", __name__)  # Changed from 'api' to 'stock_blueprint'

@stock_blueprint.route("/stocks", methods=["GET"])
def get_stocks():
    stocks = list(stocks_collection.find({}, {"_id": 0}))  # Remove MongoDB ID field
    return jsonify({"stocks": stocks})

@stock_blueprint.route("/user/<int:user_id>", methods=["GET"])
def get_user_data(user_id):
    user = users_collection.find_one({"user_id": user_id}, {"_id": 0})
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404
