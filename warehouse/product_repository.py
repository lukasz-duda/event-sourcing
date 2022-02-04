from typing import Dict
from shared.event_store import EventStore
from warehouse.product import Product

class ProductRepository:
    
    __storage: EventStore

    def __init__(self, storage: EventStore) -> None:
        super().__init__()
        self.__storage = storage

    def save(self, product: Product, expected_version: int) -> None:
        self.__storage.save_events(product.sku, product.changes, expected_version)

    def get(self, sku: str) -> Product:
        events = self.__storage.get_events_for_aggregate(sku)
        product = Product()
        product.load(events)
        return product