import unittest
import requests


class TestFlaskApiUsingRequests(unittest.TestCase):
    def test_hello_world(self):
        response = requests.get('http://localhost:5000')
        self.assertEqual(response.json(), {'hello': 'world'})


if __name__ == "__main__":
    unittest.main()
