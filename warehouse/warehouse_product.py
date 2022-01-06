from warehouse.result import Result


class WarehouseProduct:

    events = []
    
    def __init__(self, sku: str) -> None:
        self.sku = sku
        self.quantityOnHand = 0

    def receive(self, quantity: int) -> None:
        self.quantityOnHand += quantity

    def adjust_inventory(self, quantity: int, reason: str) -> None:
        self.quantityOnHand += quantity

    def ship(self, quantity: int) -> Result:
        if(self.quantityOnHand < quantity):
            return Result.fail('Not enough quantity on hand')

        self.quantityOnHand -= quantity

        return Result.ok()