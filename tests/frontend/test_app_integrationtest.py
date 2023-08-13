"""Integration tests for the frontend app."""

import unittest
from unittest.mock import patch, Mock
from applications.frontend.app import app


@DeprecationWarning
class TestApp(unittest.TestCase):
    """Integration tests for the frontend app."""

    def setUp(self):
        """Set up the test client"""
        self.app = app.test_client()
        self.app.testing = True

    @patch('psycopg2.connect')
    def test_index_with_weather_data(self, mock_connect):
        """Test that the index page shows weather data"""
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            ('Denver', 20, 80, 'Cloudy', '01d', '2023-08-11 12:00:00'),
            ('Boulder', 25, 75, 'Sunny', '02d', '2023-08-11 12:00:00')
        ]

        mock_connect.return_value.cursor.return_value = mock_cursor

        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

        rendered_html = response.get_data(as_text=True)

        self.assertIn('3-Day Weather Forecast App', rendered_html)
        self.assertIn('Boulder Forecast', rendered_html)
        self.assertIn('Denver Forecast', rendered_html)


if __name__ == '__main__':
    unittest.main()
