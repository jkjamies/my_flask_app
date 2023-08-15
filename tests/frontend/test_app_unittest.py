"""Unit tests for the frontend app."""

import json
import unittest
from applications.frontend.app import app


class TestApp(unittest.TestCase):
    """Unit tests for the frontend app. [Deprecated]"""

    def setUp(self):
        """Set up the test client"""
        self.app = app.test_client()

    def test_health_check(self):
        """Test that the health check endpoint works as expected"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), "")

    def test_metrics_endpoint(self):
        """Test the /metrics endpoint"""
        response = self.app.get('/metrics')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('requests_per_second', data)
        self.assertIsInstance(data['requests_per_second'], (int, float))
        self.assertIn('prometheus_data', data)
        self.assertIsInstance(data['prometheus_data'], str)


if __name__ == '__main__':
    unittest.main()
