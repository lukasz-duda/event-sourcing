class WarehouseProduct:

    events = []
    
    def __init__(self, sku):
        self.sku = sku
        self.quantity = 0

    def receive(self, quantity):
        self.quantity += quantity

    def adjust_inventory(self, quantity, reason):
        self.quantity += quantity

    def ship(self, quantity):
        self.quantity -= quantity