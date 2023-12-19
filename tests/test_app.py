import unittest
from src.internal import app


class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config["MONGODB_SETTINGS"] = [
            {
                "db": "m7011e-test",
                "host": "localhost",
                "port": 27017,
                "alias": "default",
            }
        ]
        self.app = app.test_client()

    def test_home_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()