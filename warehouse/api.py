from fake_bus import FakeBus
from service_locator import ServiceLocator
from warehouse.command_handlers import CommandHandlers
from warehouse.commands.receive_product_command import ReceiveProductCommand
from warehouse.event_store import EventStore
from warehouse.events.product_received import ProductReceived
from warehouse.product_repository import ProductRepository
from warehouse.read_model import FakeDatabase, InventoryItemDetailsDto, InventoryItemDetailsView
from warehouse.commands.receive_product_command import ReceiveProductCommand
from service_locator import ServiceLocator
from marshmallow import Schema, fields
from flask_restful import Api, Resource
from flask_apispec.views import MethodResource
from flask_apispec import FlaskApiSpec, marshal_with, doc, use_kwargs

def register_warehouse(api: Api, docs: FlaskApiSpec):
    database = FakeDatabase()
    database.save_details(InventoryItemDetailsDto('abc', 0))
    bus = FakeBus()
    storage = EventStore(bus)
    repository = ProductRepository(storage)
    commands = CommandHandlers(repository)
    bus.register_handler(ReceiveProductCommand, commands.handle_receive_product)
    details = InventoryItemDetailsView(database)
    bus.register_handler(ProductReceived, details.handle_product_received)
    ServiceLocator.bus = bus
    ServiceLocator.details = details

    api.add_resource(ReceiveProductResource, '/products/<sku>/receive')
    docs.register(ReceiveProductResource)

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
        view = ServiceLocator.details.get_details_item(sku)
        return view