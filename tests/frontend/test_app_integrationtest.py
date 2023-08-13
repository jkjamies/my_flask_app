"""Integration tests for the frontend app."""

import unittest
from unittest.mock import patch, MagicMock, Mock
from applications.frontend.app import app, get_db_connection


class TestApp(unittest.TestCase):
    """Integration tests for the frontend app."""

    def setUp(self):
        """Set up the test client"""
        self.app = app.test_client()
        self.app.testing = True

    def test_get_db_connection(self):
        """Test that we can get a connection to the database"""
        with (patch('applications.frontend.app.psycopg2.connect') as
              mock_connect):
            connection = MagicMock()
            mock_connect.return_value = connection
            result = get_db_connection()
            self.assertEqual(result, connection)

    @patch('psycopg2.connect')
    def test_index_with_weather_data(self, mock_connect):
        """Test that the index page shows weather data"""
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            ('Denver', 20, 80, 'Cloudy', '01d', '2023-08-11 12:00:00'),
            ('Boulder', 25, 75, 'Sunny', '02d', '2023-08-11 13:00:00')
        ]

        mock_connect.return_value.cursor.return_value = mock_cursor

        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

        rendered_html = response.get_data(as_text=True)

        self.assertIn('3-Day Weather Forecast App', rendered_html)
        self.assertIn('Boulder Forecast', rendered_html)
        self.assertIn('Denver Forecast', rendered_html)

    @patch('psycopg2.connect')
    def test_index_without_weather_data(self, mock_get_db_connection):
        """Test that the index page shows a message when there is no weather"""
        mock_cursor = mock_get_db_connection.return_value.cursor
        mock_cursor.fetchall.return_value = []

        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'3-Day Weather Forecast App', response.data)
        self.assertIn(b'No weather data available.', response.data)


if __name__ == '__main__':
    unittest.main()
