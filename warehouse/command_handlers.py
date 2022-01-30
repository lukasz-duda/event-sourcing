from warehouse.commands import AdjustInventoryCommand, ReceiveProductCommand, RegisterProductCommand, ShipProductCommand
from warehouse.product import Product
from warehouse.product_repository import ProductRepository

class CommandHandlers:

    __repository: ProductRepository

    def __init__(self, repository: ProductRepository) -> None:
        self.__repository = repository

    def handle_register_product(self, command: RegisterProductCommand) -> None:
        newProduct = Product()
        newProduct.register(command.sku)
        self.__repository.save(newProduct)

    def handle_receive_product(self, command: ReceiveProductCommand) -> None:
        product = self.__repository.get(command.sku)
        product.receive(command.quantity)
        self.__repository.save(product)

    def handle_ship_product(self, command: ShipProductCommand) -> None:
        product = self.__repository.get(command.sku)
        product.ship(command.quantity)
        self.__repository.save(product)

    def handle_adjust_inventory(self, command: AdjustInventoryCommand) -> None:
        product = self.__repository.get(command.sku)
        product.adjust_inventory(command.quantity)
        self.__repository.save(product)