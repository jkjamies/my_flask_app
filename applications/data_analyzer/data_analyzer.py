import os
from datetime import datetime
import psycopg2


class DataAnalyzer:
    def __init__(self):
        self.DATABASE_URL = os.environ.get("DATABASE_URL")
        self.connection = None

    def _get_db_connection(self):
        if not self.connection:
            self.connection = psycopg2.connect(self.DATABASE_URL,
                                               sslmode='require')
        return self.connection

    def _format_date(self, dt_txt: str):
        formatted_date = (datetime.strptime(dt_txt, '%Y-%m-%d %H:%M:%S')
                          .strftime('%A, %B %d, %Y %I:%M %p')
                          .replace(" 0", " "))
        return formatted_date

    def get_weather_data(self):
        """Get weather data from the database"""
        connection = self._get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT city, temperature, humidity, description, icon, timestamp "
            "FROM weather_data"
        )
        entries = cursor.fetchall()

        weather_data = {}

        for entry in entries:
            city, temperature, humidity, description, icon, timestamp = entry

            forecast_entry = {
                'city': city,
                'date': self._format_date(str(timestamp)),
                'temperature': temperature,
                'humidity': humidity,
                'description': description,
                'icon': self._get_icon_url(icon),
            }

            if city not in weather_data:
                weather_data[city] = []

            weather_data[city].append(forecast_entry)

        cursor.close()
        return weather_data

    def _get_icon_url(self, icon_code):
        return f"https://openweathermap.org/img/wn/{icon_code}.png"
