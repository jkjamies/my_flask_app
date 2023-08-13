"""Analyze weather data from the database"""

import os
from datetime import datetime
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")


class DataAnalyzer:
    """Analyze weather data from the database"""

    def __init__(self):
        """Initialize the DataAnalyzer"""
        self.connection = None

    def get_db_connection(self):
        """Get a database connection"""
        if not self.connection:
            self.connection = psycopg2.connect(DATABASE_URL,
                                               sslmode='require')
        return self.connection

    def format_date(self, dt_txt: str):
        """Format a date"""
        formatted_date = (datetime.strptime(dt_txt, '%Y-%m-%d %H:%M:%S')
                          .strftime('%A, %B %d, %Y %I:%M %p')
                          .replace(" 0", " "))
        return formatted_date

    def get_weather_data(self):
        """Get weather data from the database"""
        connection = self.get_db_connection()
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
                'date': self.format_date(str(timestamp)),
                'temperature': temperature,
                'humidity': humidity,
                'description': description,
                'icon': self.get_icon_url(icon),
            }

            if city not in weather_data:
                weather_data[city] = []

            weather_data[city].append(forecast_entry)

        cursor.close()
        return weather_data

    def get_icon_url(self, icon_code):
        """Get the icon url for a given icon code"""
        return f"https://openweathermap.org/img/wn/{icon_code}.png"
