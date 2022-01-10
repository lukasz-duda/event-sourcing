from datetime import datetime
from warehouse.events.event import Event

class InventoryAdjusted(Event):

    _sku: str
    _quantity: int
    _reason: str

    def __init__(self, sku: str, quantity: int, reason: str, timestamp: datetime) -> None:
        super().__init__('InventoryAdjusted', timestamp)
        self._sku = sku
        self._quantity = quantity
        self._reason = reason
    
    @property
    def sku(self) -> str:
        return self._sku

    @property
    def quantity(self) -> int:
        return self._quantity
    
    @property
    def reason(self) -> str:
        return self._reason