from flask import Blueprint, render_template
from flask_login import login_required, current_user
from database import investments_collection

dashboard = Blueprint("dashboard", __name__)

@dashboard.route("/dashboard")
@login_required
def dashboard_page():
    user_investments = list(investments_collection.find({"user_email": current_user.email}))
    
    # Simulated data (Replace with real API data)
    stock_data = {"AAPL": 150, "TSLA": 800}
    clustering_data = {"Cluster": "Low Risk"}
    recommendations = ["GOOG", "AMZN"]

    return render_template(
        "dashboard.html",
        investments=user_investments,
        stock_data=stock_data,
        clustering_data=clustering_data,
        recommendations=recommendations
    )
