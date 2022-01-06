from datetime import datetime
from warehouse.aggregate_root import AggregateRoot
from warehouse.event import Event
from warehouse.inventory_adjusted import InventoryAdjusted
from warehouse.product_received import ProductReceived
from warehouse.product_shipped import ProductShipped
from warehouse.result import Result

class WarehouseProduct(AggregateRoot):

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
        if(event._event_type in ['ProductReceived', 'InventoryAdjusted']):
            self._quantityOnHand += event.quantity
        if(event._event_type == 'ProductShipped'):
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