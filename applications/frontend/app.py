"""Flask application for the frontend of the weather app"""

import os
from datetime import datetime
from flask import Flask, render_template
from dotenv import load_dotenv
import psycopg2

load_dotenv()

app = Flask(__name__)

OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
DATABASE_URL = os.environ.get("DATABASE_URL")


def get_db_connection():
    """Get a connection to the database"""
    return psycopg2.connect(DATABASE_URL, sslmode='require')


def get_icon_url(icon_code):
    """Generate the icon URL based on the icon code"""
    return f"https://openweathermap.org/img/wn/{icon_code}.png"


@app.route('/')
def index():
    """Show the index page with weather data"""
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT DISTINCT city FROM weather_data")
    cities = [row[0] for row in cursor.fetchall()]

    weather_data = {}

    for city in cities:
        query = (
            f"SELECT city, "
            f"temperature,"
            f" humidity, "
            f"description, "
            f"icon, "
            f"timestamp "
            f"FROM weather_data "
            f"WHERE city = '{city}'"
        )
        cursor.execute(query)
        entries = cursor.fetchall()

        city_forecast = []
        for entry in entries:
            city, temperature, humidity, description, icon, timestamp = entry
            icon = get_icon_url(icon)

            forecast_entry = {
                'city': city,
                'date': format_date(str(timestamp)),
                'temperature': temperature,
                'humidity': humidity,
                'description': description,
                'icon': icon,
            }

            city_forecast.append(forecast_entry)

        weather_data[city] = city_forecast

    cursor.close()
    connection.close()

    return render_template('index.html', weather_data=weather_data)


def format_date(dt_txt: str):
    """Format the date for friendly reading"""
    formatted_date = (datetime.strptime(dt_txt, '%Y-%m-%d %H:%M:%S')
                      .strftime('%A, %B %d, %Y %I:%M %p')
                      .replace(" 0", " "))
    return formatted_date


if __name__ == '__main__':
    app.run(debug=True)
