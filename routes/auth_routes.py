from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
from pymongo import MongoClient

bcrypt = Bcrypt()
client = MongoClient("mongodb://localhost:27017/")
db = client["customer_segmentation"]
users_collection = db["users"]

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = users_collection.find_one({"email": email})

        if user and bcrypt.check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')

    return render_template('login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

        if users_collection.find_one({"email": email}):
            flash('Email already exists', 'warning')
        else:
            users_collection.insert_one({"email": email, "password": password})
            flash('Account created! Please log in.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('signup.html')
