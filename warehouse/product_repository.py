from typing import Dict
from shared.event_store import EventStore
from warehouse.product import Product

class ProductRepository:
    
    __products: Dict[str, Product]
    __storage: EventStore

    def __init__(self, storage: EventStore) -> None:
        super().__init__()
        self.__products = dict()
        self.__storage = storage

    def save(self, product: Product) -> None:
        self.__products[product.sku] = product
        self.__storage.save_events(product.sku, product.changes)

    def get(self, sku: str) -> Product:
        events = self.__storage.get_events_for_aggregate(sku)
        product = Product(sku)
        product.load(events)
        return product