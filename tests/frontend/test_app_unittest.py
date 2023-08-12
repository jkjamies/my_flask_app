"""Test the frontend.py file using unit test."""

import unittest
from applications.frontend.app import app


class TestApp(unittest.TestCase):
    """Test the frontend.py file using unit test."""

    def setUp(self):
        """Set up the test client."""
        self.app = app.test_client()

    def test_main_route(self):
        """Test the main route."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'<form action="/echo_user_input" method="POST">',
            response.data
        )


if __name__ == '__main__':
    unittest.main()
