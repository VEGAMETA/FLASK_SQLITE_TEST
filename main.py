from typing import Tuple
from utils.weather import WeatherAPI
from config import DATABASE, WEATHER_API_KEY
from misc.users_table import create_and_fill_users_table
from flask import Flask, request, jsonify, Response

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite+aiosqlite:///' + DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/update_balance')
async def update_balance() -> Tuple[Response, int]:
    """
    Route for balance updating
    :return:
    """
    from models.user import User
    from models.base import async_session
    
    user_id: int = int(request.args.get('userId'))
    city: str = request.args.get('city')

    temperature = weather.fetch_weather(city)
    if not temperature:
        return jsonify({'error': 'Failed to retrieve weather data.'}), 500
    
    async with async_session() as session:
        async with session.begin():
            user = User.get_user_by_id(user_id, session)

            if not user:
                return jsonify({'error': 'User not found.'}), 404

            try:
                user.update_balance(user.balance + temperature)
                session.commit()
                return jsonify({'message': 'Balance updated successfully.'}), 200
            except Exception as e:
                return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    weather = WeatherAPI(WEATHER_API_KEY)
    create_and_fill_users_table()
    app.run(debug=True, port=5000)
