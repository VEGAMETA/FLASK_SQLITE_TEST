from typing import Tuple
from models.base import db
from models.user import User
from utils.weather import WeatherAPI
from utils.thread_lock import locking
from config import DATABASE, WEATHER_API_KEY
from misc.users_table import create_and_fill_users_table
from flask import Flask, request, jsonify, Response

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/update_balance')
def update_balance() -> Tuple[Response, int]:
    """
    Route for balance updating
    :return:
    """
    user_id: int = int(request.args.get('userId'))
    city: str = request.args.get('city')
    temperature = weather.fetch_weather(city)

    if not temperature:
        # User receives 500 Error if there are any problems with WeatherAPI
        return jsonify({'error': 'Failed to fetch weather data.'}), 500
    return get_user_and_update_balance(user_id, temperature)


# Lock is required for Sqlite3 to block reading and committing appropriate data only
@locking
def get_user_and_update_balance(user_id, temperature):
    """
    Function gets and updates user's balance with thread locking to ensure data integrity and security
    :param user_id:
    :param temperature:
    :return:
    """
    user: User = User.get_user_by_id(user_id)
    if not user:
        # User receives 404 Error if there is no such user
        return jsonify({'error': 'User not found.'}), 404

    new_balance = user.balance + temperature
    if new_balance < 0:
        # User receives 400 Error if user balance is insufficient
        return jsonify({'error': 'Insufficient balance.'}), 400

    user.update_balance(new_balance)
    # User receives 200 (Successful response)
    return jsonify({'message': 'Balance updated successfully.'}), 200


if __name__ == '__main__':
    weather = WeatherAPI(WEATHER_API_KEY)
    create_and_fill_users_table(app, db)
    app.run(debug=True)
