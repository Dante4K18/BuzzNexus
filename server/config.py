import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key_here')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://localhost/connectsphere')
    BCRYPT_LOG_ROUNDS = 12
    SESSION_COOKIE_NAME = 'connectsphere_session'
    SESSION_PERMANENT = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your_jwt_secret_key_here')
    SOCKETIO_MESSAGE_QUEUE = os.environ.get('SOCKETIO_MESSAGE_QUEUE', 'redis://localhost:6379/0')

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'

class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL', 'postgresql://localhost/test_connectsphere')
