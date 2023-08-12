import unittest
from app import app


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_main_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'<form action="/echo_user_input" method="POST">',
            response.data
        )


if __name__ == '__main__':
    unittest.main()
