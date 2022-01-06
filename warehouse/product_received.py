from datetime import datetime
from warehouse.event import Event

class ProductReceived(Event):

    sku: str
    quantity: int

    def __init__(self, sku: str, quantity: int, timestamp: datetime) -> None:
        super().__init__(timestamp)
        self.sku = sku
        self.quantity = quantity