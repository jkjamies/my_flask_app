"""Integration tests for the app."""

import unittest
from app import app


class TestApp(unittest.TestCase):
    """Integration tests for the app."""

    def test_submit_form_and_echo(self):
        """Test submit form and echo."""
        client = app.test_client()

        response = client.post(
            '/echo_user_input',
            data={'user_input': 'Integration test input'}
        )
        assert response.status_code == 200

        expected_output = "You entered: Integration test input"
        assert expected_output.encode() in response.data


if __name__ == '__main__':
    unittest.main()
