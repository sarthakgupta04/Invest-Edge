from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from .auth import auth as auth_blueprint
from .database import db
from .models import User

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sarthak:sarthak123@localhost/investedge'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'UtEEVE@1'

    # Setup CORS specifically for the auth routes, allow credentials for secure cookies
    CORS(app, supports_credentials=True, resources={r"/app/auth/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

    db.init_app(app)

    # Initialize LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    @app.route('/')
    def home():
        return jsonify(message="Welcome to InvestEdge!")

    @app.route('/app/auth/register', methods=['POST'])
    def register():
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not all([username, email, password]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            return jsonify({'error': 'Username or email already exists'}), 409
        
        new_user = User(username=username, email=email)
        new_user.set_password(password)  # Hash the password securely
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 201

    return app
