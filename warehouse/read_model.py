from typing import Dict
from warehouse.events import ProductReceived, ProductRegistered
from shared.not_found_exception import NotFoundException

class InventoryItemDetailsDto:

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

    __details: Dict[str, InventoryItemDetailsDto]

    def __init__(self) -> None:
        self.__details = dict()

    def save_details(self, details: InventoryItemDetailsDto):
        self.__details[details.sku] = details

    def get_details(self, sku: str) -> InventoryItemDetailsDto:
        if sku in self.__details:
            return self.__details[sku]
        else:
            raise NotFoundException
        
class InventoryItemDetailsView:

    __database: FakeDatabase

    def __init__(self, database: FakeDatabase) -> None:
        self.__database = database

    def handle_product_registered(self, message: ProductRegistered) -> None:
        new_inventory_item = InventoryItemDetailsDto(sku=message.sku, current_quantity=0)
        self.__database.save_details(new_inventory_item)

    def handle_product_received(self, message: ProductReceived) -> None:
        details = self.__database.get_details(message.sku)
        inventory_item = InventoryItemDetailsDto(message.sku, details.current_quantity + message.quantity)
        self.__database.save_details(inventory_item)

class ReadModelFacade:

    __database: FakeDatabase

    def __init__(self, database: FakeDatabase) -> None:
        self.__database = database

    def get_inventory_item_details(self, sku: str) -> InventoryItemDetailsDto:
        return self.__database.get_details(sku)