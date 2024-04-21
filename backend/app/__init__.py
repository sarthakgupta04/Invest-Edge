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
    app.config['SECRET_KEY'] = 'UtEEVE@1'  # Your secret key for session handling

    # Setup CORS - This will allow all domains for all routes
    CORS(app)

    db.init_app(app)

    # Initialize LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Specify the login view
    login_manager.init_app(app)

    # User loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    @app.route('/')
    def home():
        return jsonify(message="Welcome to InvestEdge!")

    # Define the registration route
    @app.route('/app/auth/register', methods=['POST'])
    def register():
        # Example of handling registration
        data = request.get_json()  # Get data from POST request
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        if not all([username, email, password]):
            return jsonify({'error': 'Missing data'}), 400
        
        # Here you would add logic to check if the user already exists and handle password hashing

        new_user = User(username=username, email=email, password=password)  # Assuming the User model has these fields
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({'message': 'User registered successfully'}), 201

    return app
