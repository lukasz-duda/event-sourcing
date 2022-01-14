from flask import Flask, request, jsonify
from flask.helpers import make_response
from service_locator import ServiceLocator
from warehouse.command_handlers import CommandHandlers
from warehouse.commands.receive_product_command import ReceiveProductCommand
from warehouse.events.product_received import ProductReceived
from warehouse.product_repository import ProductRepository
from warehouse.read_model import FakeDatabase, InventoryItemDetailsDto, InventoryItemDetailsView

app = Flask(__name__)

database = FakeDatabase()
database.save_details(InventoryItemDetailsDto('abc', 0))
repository = ProductRepository()
commands = CommandHandlers(repository)
ServiceLocator.bus.register_handler(ReceiveProductCommand, commands.handle_receive_product)
details = InventoryItemDetailsView(database)
ServiceLocator.bus.register_handler(ProductReceived, details.handle_product_received)

@app.route('/products/receive', methods=['POST'])
def receive_product():
    json = request.get_json()
    sku = json['sku']
    quantity = json['quantity']
    command = ReceiveProductCommand(sku, quantity)
    ServiceLocator.bus.send(command)
    view = details.get_details_item(sku)
    return jsonify(sku=view.sku, quantity=view.current_quantity)