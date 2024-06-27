from flask_restful import Resource, reqparse
from flask import request
from ..schemas import servers_schema, servers_list_schema
from ..utils.db import get_db_connection
from flask_jwt_extended import jwt_required

class ServerListResource(Resource):

    # http://192.168.1.24:1133/api/server_list

    @jwt_required()
    def get(self):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT name, ip, area_code, area_code_cn, record_date FROM servers")
        servers = cursor.fetchall()
        # print(servers)
        cursor.close()
        connection.close()
        result = servers_list_schema.dump(servers)
        return result, 200

