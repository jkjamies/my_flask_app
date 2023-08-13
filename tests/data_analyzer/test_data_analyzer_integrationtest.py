"""Unit tests for the data collector app."""

import unittest
from unittest.mock import patch, Mock
from applications.data_analyzer.data_analyzer import DataAnalyzer


class TestDataAnalyzerIntegrationTest(unittest.TestCase):
    """Integration tests for the data analyzer app."""

    @patch("psycopg2.connect")
    def test_get_weather_data_with_data(self, mock_connect):
        """Test that the get_weather_data function works as expected"""
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            ('Denver', 20, 80, 'Cloudy', '01d', '2023-08-11 12:00:00'),
            ('Boulder', 25, 75, 'Sunny', '02d', '2023-08-11 12:00:00')
        ]
        mock_connect.return_value.cursor.return_value = mock_cursor

        data_analyzer = DataAnalyzer()
        weather_data = data_analyzer.get_weather_data()

        self.assertEqual(len(weather_data), 2)
        self.assertIn('Denver', weather_data)
        self.assertIn('Boulder', weather_data)
        self.assertEqual(len(weather_data['Denver']), 1)
        self.assertEqual(len(weather_data['Boulder']), 1)

    @patch("psycopg2.connect")
    def test_get_weather_data_without_data(self, mock_connect):
        """Test that the get_weather_data function works as expected"""
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = []
        mock_connect.return_value.cursor.return_value = mock_cursor

        data_analyzer = DataAnalyzer()
        weather_data = data_analyzer.get_weather_data()

        self.assertEqual(len(weather_data), 0)


if __name__ == '__main__':
    unittest.main()
