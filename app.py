from fake_bus import FakeBus
from service_locator import ServiceLocator
from warehouse.api import register_warehouse
from flask import Flask
from flask_restful import Api
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
    return app