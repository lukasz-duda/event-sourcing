from warehouse.warehouse_product import WarehouseProduct

class WarehouseProductRepository:
    
    _streams = []

    def get(self, sku: str) -> WarehouseProduct:
        return WarehouseProduct(sku)