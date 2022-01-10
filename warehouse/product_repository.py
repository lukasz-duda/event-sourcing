from warehouse.product import Product

class ProductRepository:
    
    __streams = []

    def get(self, sku: str) -> Product:
        return Product(sku)