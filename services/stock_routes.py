from flask import Blueprint, jsonify
from services.stock_service import get_stock_data

stock_bp = Blueprint('stocks', __name__)

@stock_bp.route('/<symbol>', methods=['GET'])
def fetch_stock(symbol):
    data = get_stock_data(symbol)
    return jsonify(data)
