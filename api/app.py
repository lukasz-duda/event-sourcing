from shared.event_store import AggregateNotFoundException, ConcurrencyException
from warehouse.api import register_warehouse
from flask import Flask
from flask_restful import Api, abort
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec

def create_app():
    app = Flask(__name__)
    api = Api(app)

    app.config.update({
        'APISPEC_SPEC': APISpec(title='Warehouse', version='v1', plugins=[MarshmallowPlugin()], openapi_version='2.0'),
        'APISPEC_SWAGGER_URL': '/swagger.json',
        'APISPEC_SWAGGER_UI_URL': '/'
    })

    docs = FlaskApiSpec(app)

    register_warehouse(api, docs)

    @app.errorhandler(AggregateNotFoundException)
    def handle_aggregate_not_found_exception(e):
        abort(404)

    @app.errorhandler(ConcurrencyException)
    def handle_concurrency_exception(e):
        abort(409)

    return app