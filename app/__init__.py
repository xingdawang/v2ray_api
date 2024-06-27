from flask import Flask
from flask_restful import Api
from .config import Config
from flask_jwt_extended import JWTManager

from .resources.server import ServerResource
from .resources.server_list import ServerListResource
from .resources.operator import OperatorResource
from .resources.token import TokenResource



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    api = Api(app)
    jwt = JWTManager(app)

    # refresh token
    api.add_resource(TokenResource, '/api/refresh_token')

    # table servers
    api.add_resource(ServerResource, '/api/server')
    api.add_resource(ServerListResource, '/api/server_list')

    # table operators
    api.add_resource(OperatorResource, '/api/operator')


    
    return app
