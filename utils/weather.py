import requests
import time


class WeatherAPI:
    """
    Class that handles openweathermap API
    """

    def __init__(self, api_key) -> None:
        self.base_url = f'https://api.openweathermap.org/data/2.5/weather?appid={api_key}&units=metric&q='
        self.cache = {}

    def get_cached_weather(self, city: str) -> int | None:
        """
        Returns cached weather data or None
        :param city:
        :return:
        """
        if city in self.cache:
            temperature, timestamp = self.cache[city]
            if time.monotonic() - timestamp <= 600:  # Cache validation within 10 minutes
                return temperature
        return None

    def fetch_weather(self, city: str) -> int | None:
        """
        Returns weather in Celsius or None in case of error
        :param city:
        :return:
        """
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
