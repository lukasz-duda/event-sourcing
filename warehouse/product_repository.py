from typing import Dict
from service_locator import ServiceLocator
from warehouse.product import Product

class ProductRepository:
    
    __products: Dict[str, Product]

    def __init__(self) -> None:
        super().__init__()
        self.__products = dict()

    def save(self, product: Product):
        for new_event in product.uncommitted_events:
            ServiceLocator.bus.publish(new_event)
        self.__products[product.sku] = product

    def get(self, sku: str) -> Product:
        if sku in self.__products:
            return self.__products[sku]
        else:
            return Product(sku)