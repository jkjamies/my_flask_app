"""Fetch and store weather data for Denver and Boulder"""

import os
import requests
import psycopg2
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
DATABASE_URL = os.environ.get("DATABASE_URL")


def fetch_weather_data(city):
    """Fetch weather data from OpenWeatherMap API"""
    url = (f'http://api.openweathermap.org/data/2.5/forecast?q={city}'
           f'&appid={OPENWEATHER_API_KEY}'
           f'&units=metric')
    response = requests.get(url, timeout=3)
    return response.json()


def store_weather_data(data):
    """Store weather data in the database"""
    connection = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = connection.cursor()

    city = data['city']['name']

    delete_query = "DELETE FROM weather_data WHERE city = %s"
    cursor.execute(delete_query, (city,))

    for entry in data['list']:
        temperature = entry['main']['temp']
        humidity = entry['main']['humidity']
        description = entry['weather'][0]['description']
        icon = entry['weather'][0]['icon']
        timestamp = entry['dt_txt']

        insert_query = (
            "INSERT INTO weather_data ("
            "city, "
            "temperature, "
            "humidity, "
            "description, "
            "icon, "
            "timestamp"
            ") VALUES ("
            "%s, %s, %s, %s, %s, %s)"
        )
        cursor.execute(
            insert_query,
            (
                city,
                temperature,
                humidity,
                description,
                icon,
                timestamp
            )
        )

    connection.commit()
    cursor.close()
    connection.close()


def main():
    """Fetch and store weather data for Denver and Boulder"""
    cities = ['Denver', 'Boulder']
    for city in cities:
        weather_data = fetch_weather_data(city)
        store_weather_data(weather_data)


if __name__ == "__main__":
    main()
