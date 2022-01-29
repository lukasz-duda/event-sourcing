from datetime import datetime
from shared.aggregate_root import AggregateRoot
from shared.event import Event
from warehouse.events import InventoryAdjusted, ProductReceived, ProductShipped

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

    def ship(self, quantity: int) -> None:
        if(self._quantityOnHand < quantity):
            raise Exception('Not enough quantity on hand')

        product_shipped = ProductShipped(self._sku, quantity, datetime.utcnow())
        self._add_event(product_shipped)