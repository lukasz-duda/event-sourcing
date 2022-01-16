from datetime import datetime
import json
from warehouse.events.event import Event

class ProductShipped(Event):

    _sku: str
    _quantity: int

    def __init__(self, sku: str, quantity: int, timestamp: datetime) -> None:
        super().__init__('ProductShipped', timestamp)
        self._sku = sku
        self._quantity = quantity
    
    @property
    def sku(self) -> str:
        return self._sku

    @property
    def quantity(self) -> int:
        return self._quantity
    
    def to_json(self) -> str:
        return json.dumps({
            "eventId": str(self.id),
            "eventType": self.event_type,
            "data": {
                "quantity": self.quantity
            }
        })