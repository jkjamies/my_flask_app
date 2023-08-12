"""Integration tests for the frontend."""

import unittest
from applications.frontend.app import app


class TestIntegration(unittest.TestCase):
    """Integration tests for the frontend."""

    def setUp(self):
        """Set up the test client."""
        self.app = app.test_client()
        self.app.testing = True

    def test_index_page(self):
        """Test the index page."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'3-Day Weather Forecast App', response.data)

    def test_get_3day_forecast_valid_city(self):
        """Test the get_3day_forecast route with valid city."""
        response = self.app.post('/get_3day_forecast',
                                 data={'city': 'New York'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'3-Day Weather Forecast for New York',
                      response.data)  # Add the state abbreviation
        self.assertIn(b'Temperature:', response.data)
        self.assertIn(b'Description:', response.data)

    def test_get_3day_forecast_invalid_city(self):
        """Test the get_3day_forecast route with invalid city."""
        response = self.app.post('/get_3day_forecast', data={'city': ''})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'City not provided', response.data)


if __name__ == '__main__':
    unittest.main()
