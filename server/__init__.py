from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
import os

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth.login"  # Redirect to login if not logged in
cors = CORS()
jwt = JWTManager()
socketio = SocketIO()

def create_app(config_filename=None):
    # Initialize the Flask application
    app = Flask(__name__, instance_relative_config=True)

    # Load config from the environment or a config file
    app.config.from_object('config.Config')
    if config_filename:
        app.config.from_pyfile(config_filename)

    # Initialize extensions with the app
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    cors.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app)

    # Register blueprints
    from .routes import main_bp, auth_bp, post_bp  # Assuming routes are divided into blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(post_bp)

    return app
