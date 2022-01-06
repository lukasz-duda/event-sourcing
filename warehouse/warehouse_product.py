from datetime import datetime
from warehouse.aggregate_root import AggregateRoot
from warehouse.product_received import ProductReceived
from warehouse.result import Result


class WarehouseProduct(AggregateRoot):

    def __init__(self, sku: str) -> None:
        self.sku = sku
        self.quantityOnHand = 0

    def receive(self, quantity: int) -> None:
        self.quantityOnHand += quantity

        product_received = ProductReceived(self.sku, quantity, datetime(2022, 1, 2, 3, 4, 5))
        self.uncommitted_events.append(product_received)

    def adjust_inventory(self, quantity: int, reason: str) -> None:
        self.quantityOnHand += quantity

    def ship(self, quantity: int) -> Result:
        if(self.quantityOnHand < quantity):
            return Result.fail('Not enough quantity on hand')

        self.quantityOnHand -= quantity

        return Result.ok()