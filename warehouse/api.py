from shared.fake_bus import FakeBus
from shared.service_locator import ServiceLocator
from warehouse.command_handlers import CommandHandlers
from warehouse.commands import AdjustInventoryCommand, ReceiveProductCommand, RegisterProductCommand, ShipProductCommand
from shared.event_store import EventStore
from warehouse.events import InventoryAdjusted, ProductReceived, ProductRegistered, ProductShipped
from warehouse.product_repository import ProductRepository
from warehouse.read_model import FakeDatabase, ProductDetailsView, ProductListView, ReadModelFacade
from warehouse.commands import ReceiveProductCommand
from marshmallow import Schema, fields
from flask_restful import Api, Resource
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
    bus.register_handler(ShipProductCommand, commands.handle_ship_product)
    bus.register_handler(AdjustInventoryCommand, commands.handle_adjust_inventory)
    details = ProductDetailsView(database)
    bus.register_handler(ProductRegistered, details.handle_product_registered)
    bus.register_handler(ProductReceived, details.handle_product_received)
    bus.register_handler(ProductShipped, details.handle_product_shipped)
    bus.register_handler(InventoryAdjusted, details.handle_inventory_adjusted)
    list = ProductListView(database)
    bus.register_handler(ProductRegistered, list.handle_product_registered)
    read_model = ReadModelFacade(database)
    ServiceLocator.bus = bus
    ServiceLocator.read_model = read_model

    api.add_resource(ProductResource, '/products/<sku>')
    api.add_resource(ReceiveProductResource, '/products/<sku>/receive')
    api.add_resource(ShipProductResource, '/products/<sku>/ship')
    api.add_resource(AdjustInventoryResource, '/products/<sku>/adjust-inventory')
    api.add_resource(ProductListResource, '/products')
    docs.register(ProductResource)
    docs.register(ReceiveProductResource)
    docs.register(ShipProductResource)
    docs.register(AdjustInventoryResource)
    docs.register(ProductListResource)

class ProductSchema(Schema):
    sku = fields.String(required=True, description='Product stock-keeping unit')
    current_quantity = fields.Integer(required=True, description='Current quantity', data_key='currentQuantity')
    version = fields.Integer(required=True, description='Version')

class ProductResource(MethodResource, Resource):

    @doc(description='Register product', tags=['Product'])
    @marshal_with(ProductSchema)
    def post(self, sku: str):
        command = RegisterProductCommand(sku)
        ServiceLocator.bus.send(command)
        return ServiceLocator.read_model.get_product(sku), 201, { 'Location': f'/products/{sku}' }

    @doc(description='Get product', tags=['Product'])
    @marshal_with(ProductSchema)
    def get(self, sku: str):
        return ServiceLocator.read_model.get_product(sku)

class ReceivedProduct(Schema):
    quantity = fields.Integer(required=True, description='Received quantity')
    original_version = fields.Integer(required=True, description='Original version', data_key='originalVersion')

class ReceiveProductResource(MethodResource, Resource):

    @doc(description='Receive product', tags=['Product'])
    @use_kwargs(ReceivedProduct)
    @marshal_with(ProductSchema)
    def post(self, sku: str, **kwargs):
        quantity = kwargs['quantity']
        original_version = kwargs['original_version']
        command = ReceiveProductCommand(sku, quantity, original_version)
        ServiceLocator.bus.send(command)
        return ServiceLocator.read_model.get_product(sku)

class ShippedProduct(Schema):
    quantity = fields.Integer(required=True, description='Shipped quantity')
    original_version = fields.Integer(required=True, description='Original version', data_key='originalVersion')

class ShipProductResource(MethodResource, Resource):

    @doc(description='Ship product', tags=['Product'])
    @use_kwargs(ShippedProduct)
    @marshal_with(ProductSchema)
    def post(self, sku: str, **kwargs):
        quantity = kwargs['quantity']
        original_version = kwargs['original_version']
        command = ShipProductCommand(sku, quantity, original_version)
        ServiceLocator.bus.send(command)
        return ServiceLocator.read_model.get_product(sku)

class InventoryAdjustment(Schema):
    quantity = fields.Integer(required=True, description='Adjusted quantity')
    reason = fields.String(required=True, description='Adjustment reason')
    original_version = fields.Integer(required=True, description='Original version', data_key='originalVersion')

class AdjustInventoryResource(MethodResource, Resource):

    @doc(description='Adjust inventory', tags=['Product'])
    @use_kwargs(InventoryAdjustment)
    @marshal_with(ProductSchema)
    def post(self, sku: str, **kwargs):
        quantity = kwargs['quantity']
        reason = kwargs['reason']
        original_version = kwargs['original_version']
        command = AdjustInventoryCommand(sku, quantity, reason, original_version)
        ServiceLocator.bus.send(command)
        return ServiceLocator.read_model.get_product(sku)

class ProductListItemSchema(Schema):
    sku = fields.String(required=True, description='Product stock-keeping unit')

class ProductListSchema(Schema):
    products = fields.List(fields.Nested(ProductListItemSchema), required=True)

class ProductListResource(MethodResource, Resource):

    @doc(description='Get products', tags=['Product'])
    @marshal_with(ProductListSchema)
    def get(self):
        return {
            "products": ServiceLocator.read_model.get_products()
        }