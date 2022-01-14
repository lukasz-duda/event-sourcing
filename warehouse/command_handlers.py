from warehouse.commands.receive_product_command import ReceiveProductCommand
from warehouse.product_repository import ProductRepository

class CommandHandlers:

    __repository: ProductRepository

    def __init__(self, repository: ProductRepository) -> None:
        self.__repository = repository

    def handle_receive_product(self, command: ReceiveProductCommand):
        product = self.__repository.get(command.sku)
        product.receive(command.quantity)
        self.__repository.save(product)