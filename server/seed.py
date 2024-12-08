from app import app, db
from models import User, Post, Friendship, Notification
from flask_bcrypt import Bcrypt
from datetime import datetime

bcrypt = Bcrypt(app)

# Helper function to create a hashed password
def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

# Initialize the database with some sample data
def seed():
    with app.app_context():
        # Clear the database before seeding
        db.drop_all()
        db.create_all()

        # Create sample users
        user1 = User(
            username='john_doe',
            _password_hash=hash_password('password123'),
            image_url='https://via.placeholder.com/150',
            bio='Hello, I am John! I love coding and coffee.'
        )

        user2 = User(
            username='jane_smith',
            _password_hash=hash_password('password456'),
            image_url='https://via.placeholder.com/150',
            bio='Hey, I am Jane. I enjoy traveling and photography.'
        )

        user3 = User(
            username='mike_lee',
            _password_hash=hash_password('password789'),
            image_url='https://via.placeholder.com/150',
            bio='Mike here! I’m a fitness enthusiast and tech lover.'
        )

        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        db.session.commit()

        # Create sample posts
        post1 = Post(
            title="My First Post",
            content="This is my first post on ConnectSphere! Excited to connect with others.",
            user_id=user1.id,
            created_at=datetime.utcnow()
        )

        post2 = Post(
            title="Exploring New Places",
            content="Had an amazing trip to the mountains last weekend. The view was breathtaking!",
            user_id=user2.id,
            created_at=datetime.utcnow()
        )

        post3 = Post(
            title="Fitness Journey",
            content="Started my fitness journey today! Let’s make it a lifestyle.",
            user_id=user3.id,
            created_at=datetime.utcnow()
        )

        db.session.add(post1)
        db.session.add(post2)
        db.session.add(post3)
        db.session.commit()

        # Create sample friendships (user1 follows user2, user2 follows user3)
        friendship1 = Friendship(follower_id=user1.id, followed_id=user2.id)
        friendship2 = Friendship(follower_id=user2.id, followed_id=user3.id)

        db.session.add(friendship1)
        db.session.add(friendship2)
        db.session.commit()

        # Create sample notifications
        notification1 = Notification(
            user_id=user2.id,
            message=f"{user1.username} has followed you.",
            created_at=datetime.utcnow(),
            read=False
        )

        notification2 = Notification(
            user_id=user3.id,
            message=f"{user2.username} has followed you.",
            created_at=datetime.utcnow(),
            read=False
        )

        db.session.add(notification1)
        db.session.add(notification2)
        db.session.commit()

        print("Database seeded successfully!")

# Run the seeding function
if __name__ == '__main__':
    seed()
