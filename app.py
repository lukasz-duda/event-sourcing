from flask import Flask, request
from flask.helpers import make_response

from service_locator import ServiceLocator
from warehouse.command_handlers import WarehouseCommandHandlers
from warehouse.commands import ReceiveProductCommand

app = Flask(__name__)

@app.route('/products/receive', methods=['POST'])
def receive_product():
    json = request.get_json()
    sku = json['sku']
    quantity = json['quantity']
    command = ReceiveProductCommand(sku, quantity)
    ServiceLocator.bus.send(command)
    return make_response()

commands = WarehouseCommandHandlers()
ServiceLocator.bus.register_handler(ReceiveProductCommand, commands.handle_receive_product)