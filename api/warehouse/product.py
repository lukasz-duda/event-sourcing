from datetime import datetime
from shared.aggregate_root import AggregateRoot
from shared.event import Event
from warehouse.events import InventoryAdjusted, ProductReceived, ProductRegistered, ProductShipped

class Product(AggregateRoot):

    __sku: str
    __quantityOnHand: int

    def __init__(self) -> None:
        super().__init__()

    @property
    def sku(self) -> str:
        return self.__sku
    
    @property
    def quantityOnHand(self) -> int:
        return self.__quantityOnHand

    def register(self, sku: str) -> None:
        product_registered = ProductRegistered(sku, datetime.utcnow())
        self._add_event(product_registered)

    def receive(self, quantity: int) -> None:
        product_received = ProductReceived(self.__sku, quantity, datetime.utcnow())
        self._add_event(product_received)

    def _apply(self, event: Event):
        if(event.event_type == 'ProductRegistered'):
            self.__apply_product_registered(event)
        if(event.event_type == 'ProductReceived'):
            self.__apply_product_received(event)
        if(event.event_type ==  'InventoryAdjusted'):
            self.__apply_inventory_adjusted(event)
        if(event.event_type == 'ProductShipped'):
            self.__apply_product_shipped(event)

    def __apply_product_registered(self, event: Event):
        self.__sku = event.sku
        self.__quantityOnHand = 0

    def __apply_product_received(self, event: Event):
        self.__quantityOnHand += event.quantity

    def __apply_inventory_adjusted(self, event: Event):
        self.__quantityOnHand += event.quantity

    def __apply_product_shipped(self, event: Event):
        self.__quantityOnHand -= event.quantity

    def adjust_inventory(self, quantity: int, reason: str) -> None:
        inventory_adjusted = InventoryAdjusted(self.__sku, quantity, reason, datetime.utcnow())
        self._add_event(inventory_adjusted)

    def ship(self, quantity: int) -> None:
        if(self.__quantityOnHand < quantity):
            raise Exception('Not enough quantity on hand')

        product_shipped = ProductShipped(self.__sku, quantity, datetime.utcnow())
        self._add_event(product_shipped)