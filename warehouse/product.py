from datetime import datetime
from warehouse.aggregate_root import AggregateRoot
from warehouse.events.event import Event
from warehouse.events.inventory_adjusted import InventoryAdjusted
from warehouse.events.product_received import ProductReceived
from warehouse.events.product_shipped import ProductShipped
from warehouse.result import Result

class Product(AggregateRoot):

    _sku: str
    _quantityOnHand: int

    def __init__(self, sku: str) -> None:
        super().__init__()
        self._sku = sku
        self._quantityOnHand = 0

    @property
    def sku(self) -> str:
        return self._sku
    
    @property
    def quantityOnHand(self) -> int:
        return self._quantityOnHand

    def receive(self, quantity: int) -> None:
        product_received = ProductReceived(self._sku, quantity, datetime.utcnow())
        self._add_event(product_received)

    def _apply(self, event: Event):
        if(event.event_type == 'ProductReceived'):
            self.__apply_product_received(event)
        if(event.event_type ==  'InventoryAdjusted'):
            self.__apply_inventory_adjusted(event)
        if(event.event_type == 'ProductShipped'):
            self.__apply_product_shipped(event)

    def __apply_product_received(self, event: Event):
            self._quantityOnHand += event.quantity

    def __apply_inventory_adjusted(self, event: Event):
            self._quantityOnHand += event.quantity

    def __apply_product_shipped(self, event: Event):
            self._quantityOnHand -= event.quantity

    def adjust_inventory(self, quantity: int, reason: str) -> None:
        inventory_adjusted = InventoryAdjusted(self._sku, quantity, reason, datetime.utcnow())
        self._add_event(inventory_adjusted)

    def ship(self, quantity: int) -> Result:
        if(self._quantityOnHand < quantity):
            return Result.fail('Not enough quantity on hand')

        product_shipped = ProductShipped(self._sku, quantity, datetime.utcnow())
        self._add_event(product_shipped)

        return Result.ok()