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
    __original_version: int

    def __init__(self, sku: str, quantity: int, original_version: int) -> None:
        self.__sku = sku
        self.__quantity = quantity
        self.__original_version = original_version

    @property
    def sku(self):
        return self.__sku;

    @property
    def quantity(self):
        return self.__quantity

    @property
    def original_version(self):
        return self.__original_version

class ShipProductCommand():

    __sku: str
    __quantity: int
    __original_version: int

    def __init__(self, sku: str, quantity: int, original_version: int) -> None:
        self.__sku = sku
        self.__quantity = quantity
        self.__original_version = original_version

    @property
    def sku(self):
        return self.__sku;

    @property
    def quantity(self):
        return self.__quantity

    @property
    def original_version(self):
        return self.__original_version

class AdjustInventoryCommand():

    __sku: str
    __quantity: int
    __reason: str
    __original_version: int

    def __init__(self, sku: str, quantity: int, reason: str, original_version: int) -> None:
        self.__sku = sku
        self.__quantity = quantity
        self.__reason = reason
        self.__original_version = original_version

    @property
    def sku(self):
        return self.__sku

    @property
    def quantity(self):
        return self.__quantity

    @property
    def reason(self):
        return self.__reason

    @property
    def original_version(self):
        return self.__original_version
    
class UnregisterProduct():

    __sku: str
    __original_version: int

    def __init__(self, sku: str, original_version: int) -> None:
        self.__sku = sku
        self.__original_version = original_version

    @property
    def sku(self):
        return self.__sku

    @property
    def original_version(self):
        return self.__original_version