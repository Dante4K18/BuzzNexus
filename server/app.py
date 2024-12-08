from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from models import db, bcrypt
import os

# Initialize the Flask app
app = Flask(__name__)

# Secret key for session management (replace with a secure key)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'supersecretkey')

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://localhost/connectsphere')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt(app)

# Enable Cross-Origin Resource Sharing for frontend communication
CORS(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    _password_hash = db.Column(db.String(128), nullable=False)
    image_url = db.Column(db.String(255), nullable=True, default='https://via.placeholder.com/150')
    bio = db.Column(db.String(500), nullable=True)
    posts = db.relationship('Post', backref='author', lazy=True)

    @property
    def password(self):
        raise AttributeError('Password is not accessible')

    @password.setter
    def password(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# Routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')
    bio = data.get('bio')
    image_url = data.get('image_url', 'https://via.placeholder.com/150')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 422

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'Username already taken'}), 422

    new_user = User(username=username, password=password, bio=bio, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    session['user_id'] = new_user.id  # Store the user ID in the session
    return jsonify({'id': new_user.id, 'username': new_user.username, 'bio': new_user.bio, 'image_url': new_user.image_url}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 422

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid username or password'}), 401

    session['user_id'] = user.id  # Store the user ID in the session
    return jsonify({'id': user.id, 'username': user.username, 'bio': user.bio, 'image_url': user.image_url}), 200

@app.route('/logout', methods=['DELETE'])
def logout():
    session.pop('user_id', None)  # Remove the user ID from the session
    return jsonify({'message': 'Logged out successfully'}), 204

@app.route('/check_session', methods=['GET'])
def check_session():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return jsonify({'id': user.id, 'username': user.username, 'bio': user.bio, 'image_url': user.image_url}), 200
    return jsonify({'error': 'User not authenticated'}), 401

@app.route('/profile', methods=['GET'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    user = User.query.get(session['user_id'])
    return jsonify({'id': user.id, 'username': user.username, 'bio': user.bio, 'image_url': user.image_url})

@app.route('/posts', methods=['GET'])
def get_posts():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401

    posts = Post.query.all()
    post_data = [{'id': post.id, 'title': post.title, 'content': post.content, 'created_at': post.created_at, 'user': {'id': post.author.id, 'username': post.author.username}} for post in posts]
    return jsonify(post_data), 200

@app.route('/posts', methods=['POST'])
def create_post():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401

    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return jsonify({'error': 'Title and content are required'}), 422

    user = User.query.get(session['user_id'])
    new_post = Post(title=title, content=content, author=user)
    db.session.add(new_post)
    db.session.commit()

    return jsonify({'id': new_post.id, 'title': new_post.title, 'content': new_post.content, 'created_at': new_post.created_at, 'user': {'id': user.id, 'username': user.username}}), 201

if __name__ == '__main__':
    db.create_all()  # Create database tables
    app.run(debug=True)
