from flask import Flask
from flask_restful import Api
from rpc import RPC
from log import LoggingMiddleware
app = Flask(__name__)
api = Api(app)
app.wsgi_app = LoggingMiddleware(app.wsgi_app)
api.add_resource(RPC, "/api/v1/rpc")