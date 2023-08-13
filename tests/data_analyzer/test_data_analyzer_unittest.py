"""Unit tests for the data analyzer app."""

import unittest
from applications.data_analyzer.data_analyzer import DataAnalyzer


class TestDataAnalyzerUnitTest(unittest.TestCase):
    """Unit tests for the data analyzer app."""

    def test_format_date(self):
        """Test that we can format a date"""
        data_analyzer = DataAnalyzer()
        formatted_date = data_analyzer.format_date("2023-08-11 12:00:00")
        self.assertEqual(formatted_date, "Friday, August 11, 2023 12:00 PM")

    def test_get_icon_url(self):
        """Test that we can get an icon url"""
        data_analyzer = DataAnalyzer()
        icon_url = data_analyzer.get_icon_url("01d")
        self.assertEqual(icon_url, "https://openweathermap.org/img/wn/01d.png")


if __name__ == '__main__':
    unittest.main()
