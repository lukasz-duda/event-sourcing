from typing import Dict
from warehouse.events import ProductReceived, ProductRegistered
from shared.not_found_exception import NotFoundException

class ProductDto:

    __sku: str
    __current_quantity: int

    def __init__(self, sku: str, current_quantity: int) -> None:
        self.__sku = sku
        self.__current_quantity = current_quantity

    @property
    def sku(self):
        return self.__sku

    @property
    def current_quantity(self):
        return self.__current_quantity

class FakeDatabase:

    __details: Dict[str, ProductDto]

    def __init__(self) -> None:
        self.__details = dict()

    def save_product(self, details: ProductDto):
        self.__details[details.sku] = details

    def get_product(self, sku: str) -> ProductDto:
        if sku in self.__details:
            return self.__details[sku]
        else:
            raise NotFoundException
        
class ProductDetailsView:

    __database: FakeDatabase

    def __init__(self, database: FakeDatabase) -> None:
        self.__database = database

    def handle_product_registered(self, message: ProductRegistered) -> None:
        new_product = ProductDto(sku=message.sku, current_quantity=0)
        self.__database.save_product(new_product)

    def handle_product_received(self, message: ProductReceived) -> None:
        product = self.__database.get_product(message.sku)
        changed_product = ProductDto(message.sku, product.current_quantity + message.quantity)
        self.__database.save_product(changed_product)

class ReadModelFacade:

    __database: FakeDatabase

    def __init__(self, database: FakeDatabase) -> None:
        self.__database = database

    def get_product(self, sku: str) -> ProductDto:
        return self.__database.get_product(sku)