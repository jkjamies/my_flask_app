"""The frontend application."""

from flask import Flask, render_template
from ..data_analyzer.data_analyzer import DataAnalyzer

app = Flask(__name__)
data_analyzer = DataAnalyzer()  # Create an instance of the DataAnalyzer


@app.route('/')
def index():
    """Render the index.html template with weather data."""
    weather_data = data_analyzer.get_weather_data()
    return render_template('index.html', weather_data=weather_data)


if __name__ == '__main__':
    app.run(debug=True)
