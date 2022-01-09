from warehouse.commands import ReceiveProductCommand
from warehouse.warehouse_product_repository import WarehouseProductRepository

class WarehouseCommandHandlers:

    __repository: WarehouseProductRepository

    def __init__(self) -> None:
        self.__repository = WarehouseProductRepository()

    def handle_receive_product(self, command: ReceiveProductCommand):
        product = self.__repository.get(command.sku)
        product.receive(command.quantity)