import requests
import time


class WeatherAPI:
    def __init__(self, api_key):
        self.base_url = f'http://api.openweathermap.org/data/2.5/weather?appid={api_key}&units=metric&q='
        self.cache = {}

    def get_cached_weather(self, city: str) -> int | None:
        if city in self.cache:
            temperature, timestamp = self.cache[city]
            if time.monotonic() - timestamp <= 600:  # Cache validation with time 10 mins
                return temperature
        return None

    def fetch_weather(self, city: str) -> int | None:
        temperature = self.get_cached_weather(city)
        if temperature:
            return temperature

        response = requests.get(self.base_url + city)
        if response.status_code == 200:  # successful weather API response
            data = response.json()
            temperature = round(data['main']['temp'])
            self.cache[city] = (temperature, time.monotonic())
            return temperature
        else:
            print(f"Failed to fetch weather data for {city}.")
            return None
