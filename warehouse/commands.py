class ReceiveProductCommand:

    __sku: str
    __quantity: int

    def __init__(self, sku: str, quantity: int) -> None:
        self.__sku = sku
        self.__quantity = quantity

    @property
    def sku(self):
        return self.__sku;

    @property
    def quantity(self):
        return self.__quantity