from warehouse.result import Result


class WarehouseProduct:

    events = []
    
    def __init__(self, sku: str) -> None:
        self.sku = sku
        self.quantity = 0

    def receive(self, quantity: int) -> None:
        self.quantity += quantity

    def adjust_inventory(self, quantity: int, reason: str) -> None:
        self.quantity += quantity

    def ship(self, quantity: int) -> Result:
        if(self.quantity < quantity):
            return Result.fail('Not enough quantity')

        self.quantity -= quantity

        return Result.ok()