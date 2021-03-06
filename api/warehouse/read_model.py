from curses.panel import version
from typing import Dict, List
from warehouse.events import ProductReceived, ProductRegistered

class ProductDto:

    __sku: str
    __current_quantity: int
    __version: int

    def __init__(self, sku: str, current_quantity: int, version: int) -> None:
        self.__sku = sku
        self.__current_quantity = current_quantity
        self.__version = version

    @property
    def sku(self):
        return self.__sku

    @property
    def current_quantity(self):
        return self.__current_quantity

    @property
    def version(self):
        return self.__version

class ProductListDto:

    __sku: str

    def __init__(self, sku: str) -> None:
        self.__sku = sku

    @property
    def sku(self):
        return self.__sku

class FakeDatabase:

    __details: Dict[str, ProductDto]
    __list: List[ProductListDto]

    def __init__(self) -> None:
        self.__details = dict()
        self.__list = []

    def save_product(self, details: ProductDto):
        self.__details[details.sku] = details

    def get_product(self, sku: str) -> ProductDto:
        return self.__details[sku]
    
    def add_list_item(self, list_item: ProductListDto):
        self.__list.append(list_item)
    
    def get_list(self) -> List[ProductListDto]:
        return self.__list
        
class ProductDetailsView:

    __database: FakeDatabase

    def __init__(self, database: FakeDatabase) -> None:
        self.__database = database

    def handle_product_registered(self, message: ProductRegistered) -> None:
        new_product = ProductDto(sku=message.sku, current_quantity=0, version=message.version)
        self.__database.save_product(new_product)

    def handle_product_received(self, message: ProductReceived) -> None:
        product = self.__database.get_product(message.sku)
        changed_product = ProductDto(message.sku, product.current_quantity + message.quantity, version=message.version)
        self.__database.save_product(changed_product)

    def handle_product_shipped(self, message: ProductReceived) -> None:
        product = self.__database.get_product(message.sku)
        changed_product = ProductDto(message.sku, product.current_quantity - message.quantity, version=message.version)
        self.__database.save_product(changed_product)

    def handle_inventory_adjusted(self, message: ProductReceived) -> None:
        product = self.__database.get_product(message.sku)
        changed_product = ProductDto(message.sku, product.current_quantity + message.quantity, version=message.version)
        self.__database.save_product(changed_product)
        
class ProductListView:

    __database: FakeDatabase

    def __init__(self, database: FakeDatabase) -> None:
        self.__database = database

    def handle_product_registered(self, message: ProductRegistered) -> None:
        list_item = ProductListDto(message.sku)
        self.__database.add_list_item(list_item)

class ReadModelFacade:

    __database: FakeDatabase

    def __init__(self, database: FakeDatabase) -> None:
        self.__database = database

    def get_product(self, sku: str) -> ProductDto:
        return self.__database.get_product(sku)

    def get_products(self) -> List[ProductListDto]:
        return self.__database.get_list()