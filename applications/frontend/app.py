from flask import Flask, jsonify, render_template
from prometheus_client import Counter, CollectorRegistry
import time
from ..data_analyzer.data_analyzer import DataAnalyzer

app = Flask(__name__)
data_analyzer = DataAnalyzer()

REQUEST_COUNT = Counter("http_requests_total", "Total number of HTTP requests",
                        ["method"], registry=CollectorRegistry())

last_request_time = time.time()
last_request_count = 0


@app.route('/')
def index():
    """Render the index.html template with weather data."""
    REQUEST_COUNT.labels(method="Requests/s").inc()
    weather_data = data_analyzer.get_weather_data()
    return render_template('index.html', weather_data=weather_data)


@app.route('/health', methods=['GET'])
def health():
    """Return a simple health check"""
    REQUEST_COUNT.labels(method="Requests/s").inc()
    return "", 200


@app.route('/metrics', methods=['GET'])
def metrics():
    """Return the prometheus metrics"""
    REQUEST_COUNT.labels(method="Requests/s").inc()
    global last_request_time, last_request_count

    current_time = time.time()
    time_difference = current_time - last_request_time

    requests_since_last_call = REQUEST_COUNT.labels(
        method="Requests/s").value.get()

    if time_difference > 0:
        requests_per_second = requests_since_last_call / time_difference
    else:
        requests_per_second = 0

    last_request_time = current_time
    last_request_count = REQUEST_COUNT.labels(method="Requests/s").value.get()

    REQUEST_COUNT.labels(method="Requests/s").value.set(0)

    response_data = {
        "requests_per_second": requests_per_second
    }

    return jsonify(response_data), 200


if __name__ == '__main__':
    app.run(debug=True)
