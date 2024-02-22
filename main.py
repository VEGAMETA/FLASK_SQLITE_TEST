import asyncio
from typing import Tuple
from models.base import db
from models.user import User
from utils.weather import WeatherAPI
from config import DATABASE, WEATHER_API_KEY
from misc.users_table import create_and_fill_users_table
from flask import Flask, request, jsonify, Response

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
users_processing: set[int] = set()


@app.route('/update_balance')
async def update_balance() -> Tuple[Response, int]:
    """
    Route for balance updating
    :return:
    """
    user_id: int = int(request.args.get('userId'))
    city: str = request.args.get('city')

    temperature = weather.fetch_weather(city)
    if not temperature:
        # User receives 500 Error in case of WeatherAPI problems
        return jsonify({'error': 'Failed to retrieve weather data.'}), 500

    while user_id in users_processing:
        await asyncio.sleep(0.005)
    users_processing.add(user_id)  # Locking for user

    try:
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
    finally:
        users_processing.remove(user_id)


if __name__ == '__main__':
    weather = WeatherAPI(WEATHER_API_KEY)
    create_and_fill_users_table(app, db)
    app.run(debug=True)
