from flask import Flask, request, jsonify
from fake_bus import FakeBus
from service_locator import ServiceLocator
from warehouse.command_handlers import CommandHandlers
from warehouse.commands.receive_product_command import ReceiveProductCommand
from warehouse.event_store import EventStore
from warehouse.events.product_received import ProductReceived
from warehouse.product_repository import ProductRepository
from warehouse.read_model import FakeDatabase, InventoryItemDetailsDto, InventoryItemDetailsView

app = Flask(__name__)

bus = FakeBus()
database = FakeDatabase()
database.save_details(InventoryItemDetailsDto('abc', 0))
storage = EventStore(bus)
repository = ProductRepository(storage)
commands = CommandHandlers(repository)
bus.register_handler(ReceiveProductCommand, commands.handle_receive_product)
details = InventoryItemDetailsView(database)
bus.register_handler(ProductReceived, details.handle_product_received)
ServiceLocator.bus = bus

@app.route('/products/<sku>/receive', methods=['POST'])
def receive_product(sku: str):
    json = request.get_json()
    quantity = json['quantity']
    command = ReceiveProductCommand(sku, quantity)
    ServiceLocator.bus.send(command)
    view = details.get_details_item(sku)
    return jsonify(sku=view.sku, quantity=view.current_quantity)