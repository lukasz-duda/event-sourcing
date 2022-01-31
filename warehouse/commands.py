class RegisterProductCommand:

    __sku: str

    def __init__(self, sku: str) -> None:
        self.__sku = sku

    @property
    def sku(self):
        return self.__sku

class ReceiveProductCommand():

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

class ShipProductCommand():

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

class AdjustInventoryCommand():

    __sku: str
    __quantity: int
    __reason: str

    def __init__(self, sku: str, quantity: int, reason: str) -> None:
        self.__sku = sku
        self.__quantity = quantity
        self.__reason = reason

    @property
    def sku(self):
        return self.__sku;

    @property
    def quantity(self):
        return self.__quantity

    @property
    def reason(self):
        return self.__reason;