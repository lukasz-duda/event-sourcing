import unittest
from urllib import response
import requests
import json

class CommandTest(unittest.TestCase):

    products_url = 'http://localhost:5000/products'

    def test_receive_product(self):
        product_created_response = self.__register_product(sku='abc')
        product_received_response_1 = self.__receive_product(sku='abc', quantity=1)
        product_received_response_2 = self.__receive_product(sku='abc', quantity=2)

        self.__assert_new_resource_current_quantity(product_created_response, expected_quantity=0)
        self.__assert_current_quantity(product_received_response_1, expected_quantity=1)
        self.__assert_current_quantity(product_received_response_2, expected_quantity=3)
        self.__assert_new_location_current_quantity(product_created_response, expected_quantity=3)
    
    def __register_product(self, sku: str) -> response:
        return requests.post(f'{self.products_url}/{sku}')
    
    def __receive_product(self, sku: str, quantity: int) -> response:
        request_data = json.dumps({ "quantity": quantity })
        headers = {'Content-Type': 'application/json'}
        return requests.post(f'{self.products_url}/{sku}/receive', data=request_data, headers=headers)

    def __assert_current_quantity(self, response: response, expected_quantity: int):
        self.assertEqual(200, response.status_code)
        response_data = json.loads(response.text)
        self.assertEqual(expected_quantity, response_data['currentQuantity'])

    def __assert_new_resource_current_quantity(self, response: response, expected_quantity: int):
        self.assertEqual(201, response.status_code)
        response_data = json.loads(response.text)
        self.assertEqual(expected_quantity, response_data['currentQuantity'])

    def __assert_new_location_current_quantity(self, response: response, expected_quantity: int):
        self.assertTrue('Location' in response.headers)
        location_response = requests.get(response.headers["Location"])
        location_data = json.loads(location_response.text)
        self.assertEqual(expected_quantity, location_data['currentQuantity'])
    
    def test_not_registered_product_not_found(self):
        response = self.__receive_product(sku='def', quantity=1)

        self.assertEqual(404, response.status_code)