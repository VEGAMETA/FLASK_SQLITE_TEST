from typing import Tuple

from models.base import db
from models.user import User
from utils.weather import WeatherAPI
from misc.users_table import create_and_fill_users_table
from flask import Flask, request, jsonify, Response

app = Flask(__name__)
DATABASE = 'users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/update_balance', methods=['POST', 'GET'])
def update_balance() -> Tuple[Response, int]:
    user_id: int = int(request.args.get('userId'))
    city: str = request.args.get('city')
    user: User = User.get_user_by_id(user_id)
    if user:
        temperature = weather.fetch_weather(city)
        if temperature:
            new_balance = user.balance + temperature
            if new_balance >= 0:
                user.update_balance(new_balance)
                return jsonify({'message': 'Balance updated successfully.'}), 200
            else:
                return jsonify({'error': 'Insufficient balance.'}), 400
        else:
            return jsonify({'error': 'Failed to fetch weather data.'}), 500
    else:
        return jsonify({'error': 'User not found.'}), 404


if __name__ == '__main__':
    # Please enter your openweathermap API key
    weather_api_key = '691381671de49fade74d38e8f558ee39'
    weather = WeatherAPI(weather_api_key)
    create_and_fill_users_table(app, db)
    app.run(debug=True)
