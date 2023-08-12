"""Integration tests for the frontend."""

import unittest
from applications.frontend.app import app


class TestApp(unittest.TestCase):
    """Integration tests for the frontend."""

    def setUp(self):
        """Set up the test client."""
        self.app = app.test_client()

    def test_submit_form_and_echo(self):
        """Test submit form and echo."""
        response = self.app.post(
            '/echo_user_input',
            data={'user_input': 'Integration test input'}
        )
        assert response.status_code == 200

        expected_output = "You entered: Integration test input"
        assert expected_output.encode() in response.data


if __name__ == '__main__':
    unittest.main()
