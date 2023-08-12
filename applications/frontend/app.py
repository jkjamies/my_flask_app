"""Frontend application for weather search by city"""

import os
from datetime import datetime
from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')


@app.route('/')
def index():
    """Setting frontend index.html"""
    return render_template('index.html')


@app.route('/get_3day_forecast', methods=['POST'])
def get_3day_forecast():
    """Get the 3-day forecast"""
    city = request.form['city']

    if not city:
        return render_template('index.html', error='City not provided')

    url = (f'http://api.openweathermap.org/data/2.5/forecast?q={city}'
           f'&appid={OPENWEATHER_API_KEY}'
           f'&units=metric')
    response = requests.get(url, timeout=3000)
    data = response.json()

    if data.get('cod') != '200':
        return render_template('index.html', error='City not found')

    forecast = []
    for entry in data['list']:
        forecast_entry = {
            'date': format_date(entry['dt_txt']),
            'temperature': entry['main']['temp'],
            'description': entry['weather'][0]['description'],
            'icon': entry['weather'][0]['icon'],
        }
        forecast.append(forecast_entry)

    return render_template('index.html', city=city, forecast=forecast)


def format_date(dt_txt):
    """Format the date for friendly reading"""
    dt_object = datetime.strptime(dt_txt, '%Y-%m-%d %H:%M:%S')
    formatted_date = (dt_object.strftime('%A, %B %d, %Y %I:%M %p')
                      .replace(" 0", " "))
    return formatted_date


if __name__ == '__main__':
    app.run(debug=True)
