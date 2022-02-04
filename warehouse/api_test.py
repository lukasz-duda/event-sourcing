import unittest
from urllib import response
import requests
import json

class CommandTest(unittest.TestCase):

    __products_url = 'http://localhost:5000/products'
    __sku = 'abc'
    __last_version = -1

    def setUp(self) -> None:
        self.last_version = -1
        return super().setUp()

    def test_receive_product(self):
        product_created_response = self.__register_product()
        product_received_response_1 = self.__receive_product(quantity=1)
        product_received_response_2 = self.__receive_product(quantity=2)

        self.__assert_new_resource_current_quantity(product_created_response, expected_quantity=0)
        self.__assert_current_quantity(product_received_response_1, expected_quantity=1)
        self.__assert_current_quantity(product_received_response_2, expected_quantity=3)
        self.__assert_new_location_current_quantity(product_created_response, expected_quantity=3)
    
    def __register_product(self) -> response:
        response = requests.post(f'{self.__products_url}/{self.sku}')
        self.update_version(response)
        return response
    
    def __receive_product(self, quantity: int) -> response:
        request_data = json.dumps({ "quantity": quantity, "originalVersion": self.last_version })
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f'{self.__products_url}/{self.sku}/receive', data=request_data, headers=headers)
        self.update_version(response)
        return response
    
    @property
    def sku(self):
        return self.__sku
    
    @sku.setter
    def sku(self, value: str):
        self.__sku = value

    def update_version(self, response: response) -> None:
        if(response.ok):
            response_data = json.loads(response.text)
            self.last_version = response_data['version']
    
    @property
    def last_version(self):
        return self.__last_version
    
    @last_version.setter
    def last_version(self, value: str):
        self.__last_version = value

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
        self.sku = 'not_registered_sku'
        response = self.__receive_product(quantity=1)

        self.assertEqual(404, response.status_code)