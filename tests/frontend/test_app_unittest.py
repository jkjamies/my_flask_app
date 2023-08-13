"""Unit tests for the frontend app."""

import unittest
from applications.frontend.app import format_date


class TestApp(unittest.TestCase):
    """Unit tests for the frontend app."""

    def test_format_date(self):
        """Test that we can format a date"""
        dt_txt = '2023-08-11 12:00:00'
        formatted_date = format_date(dt_txt)
        expected_date = 'Friday, August 11, 2023 12:00 PM'
        self.assertEqual(formatted_date, expected_date)


if __name__ == '__main__':
    unittest.main()
