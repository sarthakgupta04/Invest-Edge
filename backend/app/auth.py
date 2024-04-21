from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, db
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Missing username, email, or password"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already in use"}), 409

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already in use"}), 409

    user = User(username=username, email=email)
    user.set_password(password)  # Hash the password before saving
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        login_user(user, remember=True)  # Optionally add 'remember=True' if you want to implement persistent sessions
        return jsonify({"message": "Logged in successfully!", "user": {"username": user.username, "email": user.email}})
    else:
        return jsonify({"error": "Invalid username or password"}), 401

@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200
