from datetime import datetime
from shared.fake_bus import FakeBus
from shared.service_locator import ServiceLocator
from warehouse.command_handlers import CommandHandlers
from warehouse.commands import ReceiveProductCommand, RegisterProductCommand
from shared.event_store import EventStore
from warehouse.events import ProductReceived, ProductRegistered
from shared.not_found_exception import NotFoundException
from warehouse.product_repository import ProductRepository
from warehouse.read_model import FakeDatabase, InventoryItemDetailsDto, InventoryItemDetailsView, ReadModelFacade
from warehouse.commands import ReceiveProductCommand
from marshmallow import Schema, fields
from flask_restful import Api, Resource, abort
from flask_apispec.views import MethodResource
from flask_apispec import FlaskApiSpec, marshal_with, doc, use_kwargs

def register_warehouse(api: Api, docs: FlaskApiSpec):
    database = FakeDatabase()
    bus = FakeBus()
    storage = EventStore(bus)
    repository = ProductRepository(storage)
    commands = CommandHandlers(repository)
    bus.register_handler(RegisterProductCommand, commands.handle_register_product)
    bus.register_handler(ReceiveProductCommand, commands.handle_receive_product)
    details = InventoryItemDetailsView(database)
    bus.register_handler(ProductRegistered, details.handle_product_registered)
    bus.register_handler(ProductReceived, details.handle_product_received)
    read_model = ReadModelFacade(database)
    ServiceLocator.bus = bus
    ServiceLocator.read_model = read_model

    api.add_resource(ProductResource, '/products/<sku>')
    api.add_resource(ReceiveProductResource, '/products/<sku>/receive')
    docs.register(ProductResource)
    docs.register(ReceiveProductResource)

class ProductResponseSchema(Schema):
    sku = fields.String(required=True, description="Product stock-keeping unit")
    current_quantity = fields.Integer(required=True, description="Current quantity", data_key="currentQuantity")

class ProductResource(MethodResource, Resource):

    @doc(description='Register product', tags=['Product'])
    @marshal_with(ProductResponseSchema)
    def post(self, sku: str):
        try:
            command = RegisterProductCommand(sku)
            ServiceLocator.bus.send(command)
            return ServiceLocator.read_model.get_inventory_item_details(sku)
        except NotFoundException:
            abort(404)

class ReceiveProductRequestSchema(Schema):
    quantity = fields.Integer(required=True, description="Received quantity")

class ReceiveProductResource(MethodResource, Resource):

    @doc(description='Receive product', tags=['Product'])
    @use_kwargs(ReceiveProductRequestSchema)
    @marshal_with(ProductResponseSchema)
    def post(self, sku: str, **kwargs):
        quantity = kwargs['quantity']
        command = ReceiveProductCommand(sku, quantity)
        try:
            ServiceLocator.bus.send(command)
            return ServiceLocator.read_model.get_inventory_item_details(sku)
        except NotFoundException:
            abort(404)