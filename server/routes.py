from flask import Blueprint, request, jsonify, session
from models import db, User, Post, Friendship, Notification
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError

# Initialize the Blueprint and bcrypt
auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

# Signup route
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    # Validate the data
    if not data.get('username') or not data.get('password'):
        return jsonify({"error": "Username and password are required"}), 422

    # Check if username already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username is already taken"}), 422

    try:
        user = User(
            username=data['username'],
            password=data['password'],
            image_url=data.get('image_url', 'https://via.placeholder.com/150'),
            bio=data.get('bio', '')
        )
        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id  # Save user ID in session

        return jsonify({
            "id": user.id,
            "username": user.username,
            "image_url": user.image_url,
            "bio": user.bio
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "An error occurred while creating the account"}), 500

# Login route
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not bcrypt.check_password_hash(user._password_hash, password):
        return jsonify({"error": "Invalid username or password"}), 401

    session['user_id'] = user.id

    return jsonify({
        "id": user.id,
        "username": user.username,
        "image_url": user.image_url,
        "bio": user.bio
    }), 200

# Check session route (auto-login)
@auth_bp.route('/check_session', methods=['GET'])
def check_session():
    if 'user_id' not in session:
        return jsonify({"error": "Not logged in"}), 401

    user = User.query.get(session['user_id'])

    return jsonify({
        "id": user.id,
        "username": user.username,
        "image_url": user.image_url,
        "bio": user.bio
    }), 200

# Logout route
@auth_bp.route('/logout', methods=['DELETE'])
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)
        return '', 204
    return jsonify({"error": "No user logged in"}), 401

# Create a post route
@auth_bp.route('/posts', methods=['POST'])
def create_post():
    if 'user_id' not in session:
        return jsonify({"error": "You must be logged in to create a post"}), 401

    data = request.get_json()

    if not data.get('title') or not data.get('content'):
        return jsonify({"error": "Title and content are required"}), 422

    user = User.query.get(session['user_id'])
    post = Post(
        title=data['title'],
        content=data['content'],
        user_id=user.id
    )

    db.session.add(post)
    db.session.commit()

    return jsonify({
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "created_at": post.created_at,
        "author": {
            "id": user.id,
            "username": user.username
        }
    }), 201

# Get all posts route (for home/feed)
@auth_bp.route('/posts', methods=['GET'])
def get_posts():
    if 'user_id' not in session:
        return jsonify({"error": "You must be logged in to view posts"}), 401

    posts = Post.query.all()
    posts_data = [{
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "created_at": post.created_at,
        "author": {
            "id": post.author.id,
            "username": post.author.username
        }
    } for post in posts]

    return jsonify(posts_data), 200

# Follow a user route
@auth_bp.route('/follow/<int:followed_id>', methods=['POST'])
def follow_user(followed_id):
    if 'user_id' not in session:
        return jsonify({"error": "You must be logged in to follow users"}), 401

    follower = User.query.get(session['user_id'])
    followed = User.query.get(followed_id)

    if not followed:
        return jsonify({"error": "User to follow not found"}), 404

    if follower.id == followed.id:
        return jsonify({"error": "You cannot follow yourself"}), 422

    # Check if already following
    if Friendship.query.filter_by(follower_id=follower.id, followed_id=followed.id).first():
        return jsonify({"error": "You are already following this user"}), 422

    friendship = Friendship(follower_id=follower.id, followed_id=followed.id)
    db.session.add(friendship)
    db.session.commit()

    return jsonify({
        "message": f"You are now following {followed.username}"
    }), 200

# Unfollow a user route
@auth_bp.route('/unfollow/<int:followed_id>', methods=['DELETE'])
def unfollow_user(followed_id):
    if 'user_id' not in session:
        return jsonify({"error": "You must be logged in to unfollow users"}), 401

    follower = User.query.get(session['user_id'])
    followed = User.query.get(followed_id)

    if not followed:
        return jsonify({"error": "User to unfollow not found"}), 404

    friendship = Friendship.query.filter_by(follower_id=follower.id, followed_id=followed.id).first()

    if not friendship:
        return jsonify({"error": "You are not following this user"}), 422

    db.session.delete(friendship)
    db.session.commit()

    return jsonify({
        "message": f"You have unfollowed {followed.username}"
    }), 200

# Get notifications for the logged-in user
@auth_bp.route('/notifications', methods=['GET'])
def get_notifications():
    if 'user_id' not in session:
        return jsonify({"error": "You must be logged in to view notifications"}), 401

    user = User.query.get(session['user_id'])
    notifications = Notification.query.filter_by(user_id=user.id, read=False).all()
    notifications_data = [{
        "id": notification.id,
        "message": notification.message,
        "created_at": notification.created_at
    } for notification in notifications]

    return jsonify(notifications_data), 200

# Mark notifications as read
@auth_bp.route('/notifications/read', methods=['POST'])
def mark_notifications_as_read():
    if 'user_id' not in session:
        return jsonify({"error": "You must be logged in to mark notifications"}), 401

    user = User.query.get(session['user_id'])
    notifications = Notification.query.filter_by(user_id=user.id, read=False).all()

    for notification in notifications:
        notification.read = True

    db.session.commit()

    return jsonify({"message": "Notifications marked as read"}), 200
