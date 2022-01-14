import unittest
import requests
import json

class CommandTest(unittest.TestCase):

    def test_receive_product(self):
        request_data = json.dumps({ "sku": "abc", "quantity": 5 })
        headers = {'Content-Type': 'application/json'}

        response = requests.post('http://localhost:5000/products/receive', data=request_data, headers=headers)

        self.assertEqual(200, response.status_code)
        response_data = json.loads(response.text)
        self.assertEqual(5, response_data['quantity'])