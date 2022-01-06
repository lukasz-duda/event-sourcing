from datetime import datetime
from warehouse.aggregate_root import AggregateRoot
from warehouse.event import Event
from warehouse.product_received import ProductReceived
from warehouse.result import Result


class WarehouseProduct(AggregateRoot):

    def __init__(self, sku: str) -> None:
        super().__init__()
        self.sku = sku
        self.quantityOnHand = 0

    def receive(self, quantity: int) -> None:
        product_received = ProductReceived(self.sku, quantity, datetime.utcnow())
        self.add_event(product_received)
        self.apply(product_received)

    def apply(self, event: Event):
        if(event.event_type in ['ProductReceived']):
            self.__increase_quantity(event.quantity)

    def __increase_quantity(self, quantity: int):
        self.quantityOnHand += quantity

    def adjust_inventory(self, quantity: int, reason: str) -> None:
        self.quantityOnHand += quantity

    def ship(self, quantity: int) -> Result:
        if(self.quantityOnHand < quantity):
            return Result.fail('Not enough quantity on hand')

        self.quantityOnHand -= quantity

        return Result.ok()