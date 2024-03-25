from models.base import db


class User(db.Model):
    """
    User model handle users table
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    balance = db.Column(db.Integer, nullable=False)

    def update_balance(self, balance: int) -> None:
        """
        Changing balance column for this user
        :param balance:
        :return:
        """
        if balance < 0:
            raise ValueError("Balance must be >= 0")

        self.balance = balance

    def update_username(self, username: str) -> None:
        """
        Changing username column for this user
        :param username:
        :return:
        """
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            raise ValueError("Username already exists")

        self.username = username

    @staticmethod
    def get_user_by_id(user_id: int, session) -> 'User':
        """
        Returns user by id
        :param user_id:
        :return:
        """
        return session.query(User.balance).with_for_update().filter_by(id=user_id).first()

    @staticmethod
    def add_user(username, balance) -> None:
        """
        Adds new user to the table
        :param username:
        :param balance:
        :return:
        """
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            raise ValueError("Username already exists")

        user = User(username=username, balance=balance)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def delete_user(user_id) -> None:
        """
        Removes user from the table
        :param user_id:
        :return:
        """
        user = User.get_user_by_id(user_id)
        if not user:
            raise ValueError("Username does not exists")

        db.session.delete(user)
        db.session.commit()
