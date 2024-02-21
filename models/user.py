from models.base import db, BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    balance = db.Column(db.Integer, nullable=False)

    @staticmethod
    def get_user_by_id(user_id: int) -> 'User':
        return User.query.filter_by(id=user_id).first()

    def update_balance(self, new_balance: int) -> None:
        self.balance = new_balance
        db.session.commit()
