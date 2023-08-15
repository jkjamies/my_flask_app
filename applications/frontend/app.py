"""The frontend application."""

from flask import Flask, jsonify, render_template
from prometheus_client import Counter, CollectorRegistry, generate_latest
import time
from ..data_analyzer.data_analyzer import DataAnalyzer

app = Flask(__name__)
data_analyzer = DataAnalyzer()

registry = CollectorRegistry()
REQUEST_COUNT = Counter("http_requests_per_second",
                        "Requests per second since app start",
                        ["method"], registry=registry)
start_time = time.time()


@app.route('/')
def index():
    """Render the index.html template with weather data."""
    weather_data = data_analyzer.get_weather_data()
    return render_template('index.html', weather_data=weather_data)


@app.route('/health', methods=['GET'])
def health():
    """Return a simple health check"""
    return "", 200


@app.route('/metrics', methods=['GET'])
def metrics():
    """Return the prometheus metrics"""
    current_time = time.time()
    time_difference = current_time - start_time

    total_requests = REQUEST_COUNT.labels(method="GET").value.get()

    if time_difference > 0:
        requests_per_second = total_requests / time_difference
    else:
        requests_per_second = 0

    response_data = {
        "requests_per_second": requests_per_second
    }

    metrics_data = generate_latest(registry=registry)
    response_data["prometheus_data"] = metrics_data.decode('utf-8')

    return jsonify(response_data), 200


@app.before_request
def before_request():
    REQUEST_COUNT.labels(method="GET").inc()


if __name__ == '__main__':
    app.run(debug=True)
