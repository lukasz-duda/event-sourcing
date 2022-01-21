from fake_bus import FakeBus
from service_locator import ServiceLocator
from warehouse.command_handlers import CommandHandlers
from warehouse.commands.receive_product_command import ReceiveProductCommand
from warehouse.event_store import EventStore
from warehouse.events.product_received import ProductReceived
from warehouse.product_repository import ProductRepository
from warehouse.read_model import FakeDatabase, InventoryItemDetailsDto, InventoryItemDetailsView

from flask import Flask
from marshmallow import Schema, fields
from flask_restful import Resource, Api
from flask_apispec.views import MethodResource
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_apispec import marshal_with, doc, use_kwargs

app = Flask(__name__)
api = Api(app)

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

class ReceiveProductRequestSchema(Schema):
    quantity = fields.Integer(required=True, description="Received quantity")

class ReceiveProductResponseSchema(Schema):
    sku = fields.String(required=True, description="Product stock-keeping unit")
    current_quantity = fields.Integer(required=True, description="Current quantity", data_key="currentQuantity")

class ReceiveProductResource(MethodResource, Resource):

    @doc(description='Receive product', tags=['Product'])
    @use_kwargs(ReceiveProductRequestSchema)
    @marshal_with(ReceiveProductResponseSchema)
    def post(self, sku: str, **kwargs):
        quantity = kwargs['quantity']
        command = ReceiveProductCommand(sku, quantity)
        ServiceLocator.bus.send(command)
        view = details.get_details_item(sku)
        return view

api.add_resource(ReceiveProductResource, '/products/<sku>/receive')

app.config.update({
    'APISPEC_SPEC': APISpec(title='Warehouse', version='v1', plugins=[MarshmallowPlugin()], openapi_version='2.0'),
    'APISPEC_SWAGGER_URL': '/swagger.json',
    'APISPEC_SWAGGER_UI_URL': '/'
})

docs = FlaskApiSpec(app)
docs.register(ReceiveProductResource)