"""The frontend application."""

from flask import Flask, render_template, Response
from prometheus_client import Counter, CollectorRegistry, generate_latest
from applications.data_analyzer.data_analyzer import DataAnalyzer

app = Flask(__name__)
data_analyzer = DataAnalyzer()

registry = CollectorRegistry()
REQUEST_COUNT = Counter("http_requests_per_second",
                        "Requests per second since app start",
                        ["method"], registry=registry)


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
    metrics_data = generate_latest(registry=registry)
    return Response(metrics_data, content_type="text/plain")


@app.before_request
def before_request():
    REQUEST_COUNT.labels(method="GET").inc()


if __name__ == '__main__':
    app.run(debug=True)
