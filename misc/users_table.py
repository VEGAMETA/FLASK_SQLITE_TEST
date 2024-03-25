import random

def create_and_fill_users_table():
    """
    Creates and fills users table if it was not
    :param app:
    :param db:
    :return:
    """
    from models.user import User
    from main import app
    from models.base import db
    with app.app_context():
        db.create_all()
        if User.query.count() == 0:
            for _ in range(5):
                username = f"user{_ + 1}"
                balance = random.randint(5000, 15000)
                User.add_user(username=username, balance=balance)
