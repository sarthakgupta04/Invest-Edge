from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, db
from flask_login import login_user, logout_user, login_required, current_user

# Create a Blueprint for authentication-related operations
auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    """ Register a new user. """
    data = request.get_json()
    username = data.get('username', '').strip()
    email = data.get('email', '').strip().lower()  # Normalize the email
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Missing username, email, or password"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already in use"}), 409

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already in use"}), 409

    user = User(username=username, email=email)
    user.password_hash = generate_password_hash(password)  # Hash the password before storing
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"}), 201

@auth.route('/login', methods=['POST', 'OPTIONS'])
def login():
    """ Log in a user. """
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()

    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        login_user(user)
        return jsonify({"message": "Logged in successfully!"}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    """ Log out the current user. """
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

def _build_cors_preflight_response():
    """Builds a CORS preflight response."""
    response = make_response()
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    return response

