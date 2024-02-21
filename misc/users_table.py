import random
from models.user import User


def create_and_fill_users_table(app, db):
    with app.app_context():
        # Creates table if not
        db.create_all()

        # Check if users ar in the table
        if User.query.count() == 0:
            # Generates data for 5 users
            for _ in range(5):
                username = f"user{_ + 1}"
                balance = random.randint(5000, 15000)
                user = User(username=username, balance=balance)
                db.session.add(user)
            db.session.commit()
