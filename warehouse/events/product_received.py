from datetime import datetime
import json
from warehouse.events.event import Event

class ProductReceived(Event):

    __sku: str
    __quantity: int

    def __init__(self, sku: str, quantity: int, timestamp: datetime) -> None:
        super().__init__('ProductReceived', timestamp)
        self.__sku = sku
        self.__quantity = quantity
    
    @property
    def sku(self) -> str:
        return self.__sku

    @property
    def quantity(self) -> int:
        return self.__quantity
    
    def to_json(self) -> str:
        return json.dumps({
            "eventId": str(self.id),
            "eventType": self.event_type,
            "data": {
                "quantity": self.quantity
            }
        })