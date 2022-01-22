import unittest
from urllib import response
import requests
import json

class CommandTest(unittest.TestCase):

    def test_receive_product(self):
        response_1 = self.__receive_product(1)
        response_2 = self.__receive_product(2)

        self.__assert_current_quantity(response=response_1, expected_quantity=1)
        self.__assert_current_quantity(response=response_2, expected_quantity=3)
    
    def __receive_product(self, quantity: int) -> response:
        request_data = json.dumps({ "quantity": quantity })
        headers = {'Content-Type': 'application/json'}
        return requests.post('http://localhost:5000/products/abc/receive', data=request_data, headers=headers)

    def __assert_current_quantity(self, response: response, expected_quantity: int):
        self.assertEqual(200, response.status_code)
        response_data = json.loads(response.text)
        self.assertEqual(expected_quantity, response_data['currentQuantity'])