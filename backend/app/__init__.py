from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from .auth import auth as auth_blueprint
from .database import db
from .models import User
import os  # For environment variables

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'mysql+pymysql://sarthak:sg123@localhost/investedge')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'UtEEVE@1')

    # Setup CORS specifically for the auth routes, allowing credentials for secure cookies
    CORS(app, resources={r"/app/auth/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

    db.init_app(app)

    # Initialize LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_blueprint, url_prefix='/app/auth')  # Ensure correct blueprint prefix

    @app.route('/')
    def home():
        return jsonify(message="Welcome to InvestEdge!")

    @app.route('/app/auth/register', methods=['POST'])
    def register():
        data = request.get_json()
        username = data.get('username', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password')

        if not username or not email or not password:
            return jsonify({'error': 'Missing required fields'}), 400
        
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            return jsonify({'error': 'Username or email already exists'}), 409
        
        new_user = User(username=username, email=email)
        new_user.set_password(password)  # Ensure password is hashed
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 201

    return app
