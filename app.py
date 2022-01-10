from flask import Flask, request
from flask.helpers import make_response
from service_locator import ServiceLocator
from warehouse.command_handlers import CommandHandlers
from warehouse.commands.receive_product_command import ReceiveProductCommand
from warehouse.product_repository import ProductRepository

app = Flask(__name__)

@app.route('/products/receive', methods=['POST'])
def receive_product():
    json = request.get_json()
    sku = json['sku']
    quantity = json['quantity']
    command = ReceiveProductCommand(sku, quantity)
    ServiceLocator.bus.send(command)
    return make_response()

repository = ProductRepository()
commands = CommandHandlers(repository)
ServiceLocator.bus.register_handler(ReceiveProductCommand, commands.handle_receive_product)