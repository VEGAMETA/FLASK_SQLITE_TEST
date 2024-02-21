from models.base import db, BaseModel


class User(BaseModel):
    """
    User model handle users table
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    balance = db.Column(db.Integer, nullable=False)

    def update_balance(self, new_balance: int) -> None:
        """
        Changing balance column for this user
        :param new_balance:
        :return:
        """
        self.balance = new_balance
        db.session.commit()

    @staticmethod
    def get_user_by_id(user_id: int) -> 'User':
        """
        Returns user by id
        :param user_id:
        :return:
        """
        return User.query.filter_by(id=user_id).first()
