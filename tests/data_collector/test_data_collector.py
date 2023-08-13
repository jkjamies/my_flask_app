"""Unit tests for the data collector app."""

import unittest
from unittest.mock import patch, Mock
from applications.data_collector.fetch_and_store import fetch_weather_data, \
    store_weather_data


class TestDataCollector(unittest.TestCase):
    """Unit tests for the data collector app."""

    @patch("requests.get")
    def test_fetch_weather_data(self, mock_get):
        """Test that the fetch_weather_data function works as expected"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'city': {'name': 'Denver'},
            'list': [{'main': {'temp': 20, 'humidity': 80},
                      'weather': [{'description': 'Cloudy', 'icon': '01d'}],
                      'dt_txt': '2023-08-11 12:00:00'}]
        }
        mock_get.return_value = mock_response

        response = fetch_weather_data('Denver')

        self.assertEqual(response['city']['name'], 'Denver')
        self.assertEqual(len(response['list']), 1)
        self.assertEqual(response['list'][0]['main']['temp'], 20)
        self.assertEqual(response['list'][0]['main']['humidity'], 80)
        self.assertEqual(response['list'][0]['weather'][0]['description'],
                         'Cloudy')
        self.assertEqual(response['list'][0]['weather'][0]['icon'], '01d')
        self.assertEqual(response['list'][0]['dt_txt'], '2023-08-11 12:00:00')

    @patch("psycopg2.connect")
    @patch("psycopg2.extensions.cursor")
    def test_store_weather_data(self, mock_cursor, mock_connect):
        """Test that the store_weather_data function works as expected"""
        mock_connection = mock_connect.return_value
        mock_cursor_instance = mock_cursor.return_value

        data = {
            'city': {'name': 'Denver'},
            'list': [{'main': {'temp': 20, 'humidity': 80},
                      'weather': [{'description': 'Cloudy', 'icon': '01d'}],
                      'dt_txt': '2023-08-11 12:00:00'}]
        }

        store_weather_data(data)

        mock_connect.assert_called_once()
        mock_cursor_instance.execute.reset_mock()
        mock_connection.commit.assert_called_once()
        mock_connection.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
