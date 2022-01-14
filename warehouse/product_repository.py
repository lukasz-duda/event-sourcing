from typing import Dict
from service_locator import ServiceLocator
from warehouse.event_store import EventStore
from warehouse.product import Product

class ProductRepository:
    
    __products: Dict[str, Product]
    __storage: EventStore

    def __init__(self, storage: EventStore) -> None:
        super().__init__()
        self.__products = dict()
        self.__storage = storage

    def save(self, product: Product):
        self.__products[product.sku] = product
        self.__storage.save_events(product.sku, product.changes)

    def get(self, sku: str) -> Product:
        if sku in self.__products:
            return self.__products[sku]
        else:
            return Product(sku)