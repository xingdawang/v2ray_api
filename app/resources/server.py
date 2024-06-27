from flask_restful import Resource, reqparse
from flask import request
from ..schemas import servers_schema, servers_list_schema
from ..utils.db import get_db_connection
from flask_jwt_extended import jwt_required

class ServerResource(Resource):

    # http://192.168.1.24:1133/api/server?name=v2ray-california-7&ip=54.183.129.46&area_code=US7&area_code_cn=美区7

    @jwt_required()
    def get(self):

        # parse parameters
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='args', required=False)
        parser.add_argument('ip', type=str, location='args', required=False)
        parser.add_argument('area_code', type=str, location='args', required=False)
        parser.add_argument('area_code_cn', type=str, location='args', required=False)
        args = parser.parse_args()

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        query = "SELECT name, ip, area_code, area_code_cn, record_date FROM servers WHERE 1=1"
        filters = []

        if args['name']:
            query += " AND name = %s"
            filters.append(args['name'])
        if args['ip']:
            query += " AND ip = %s"
            filters.append(args['ip'])
        if args['area_code']:
            query += " AND area_code = %s"
            filters.append(args['area_code'])
        if args['area_code_cn']:
            query += " AND area_code_cn = %s"
            filters.append(args['area_code_cn'])

        cursor.execute(query, tuple(filters))
        server_result = cursor.fetchall()
        cursor.close()
        connection.close()

        if not server_result:
            return {'message': 'No matching records found'}, 404

        result = servers_list_schema.dump(server_result)
        return result, 200


    # use name to update ip or area_code or area_code_cn
    # POSTMAN
    # http://192.168.1.24:1133/api/server?name=v2ray-california-7&area_code_cn=美区7&area_code=US7&ip=54.183.129.46

    @jwt_required()
    def put(self):

        # parse parameters
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, location='args', help="Name cannot be blank!")
        parser.add_argument('ip', location='args', type=str)
        parser.add_argument('area_code', location='args', type=str)
        parser.add_argument('area_code_cn', location='args', type=str)
        args = parser.parse_args()

        name = args['name']
        ip = args['ip']
        area_code = args['area_code']
        area_code_cn = args['area_code_cn']

        if not (ip or area_code or area_code_cn):
            return {'message': 'No update parameters provided'}, 400

        connection = get_db_connection()
        cursor = connection.cursor()

        query = "UPDATE servers SET"
        updates = []
        values = []

        if ip:
            updates.append(" ip = %s")
            values.append(ip)
        if area_code:
            updates.append(" area_code = %s")
            values.append(area_code)
        if area_code_cn:
            updates.append(" area_code_cn = %s")
            values.append(area_code_cn)

        query += ",".join(updates) + " WHERE name = %s"
        values.append(name)

        cursor.execute(query, tuple(values))
        connection.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        connection.close()

        if rows_affected == 0:
            return {'message': 'No matching records found to update'}, 404

        return {'message': f'{rows_affected} record(s) updated'}, 200


    # POSTMAN
    # http://192.168.1.24:1133/api/server?ip=54.183.129.46

    @jwt_required()
    def delete(self):

        # parse parameters
        name = request.args.get('name')
        ip = request.args.get('ip')
        area_code = request.args.get('area_code')
        area_code_cn = request.args.get('area_code_cn')

        if not (name or ip or area_code or area_code_cn):
            return {'message': 'No parameters provided for deletion'}, 400

        connection = get_db_connection()
        cursor = connection.cursor()

        query = "DELETE FROM servers WHERE 1=1"
        filters = []

        if name:
            query += " AND name = %s"
            filters.append(name)
        if ip:
            query += " AND ip = %s"
            filters.append(ip)
        if area_code:
            query += " AND area_code = %s"
            filters.append(area_code)
        if area_code_cn:
            query += " AND area_code_cn = %s"
            filters.append(area_code_cn)

        cursor.execute(query, tuple(filters))
        connection.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        connection.close()

        if rows_affected == 0:
            return {'message': 'No matching records found to delete'}, 404

        return {'message': f'{rows_affected} record(s) deleted'}, 200


    # POSTMAN:
    # curl -X POST http://192.168.1.24:1133/api/server_list \
    # -H "Content-Type: application/json" \
    # -d '{"name": "v2ray-california-7", "ip": "54.183.129.46", "area_code": "US7", "area_code_cn": "美区7"}'

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='args', required=True, help="name cannot be blank!")
        parser.add_argument('ip', type=str, location='args', required=True, help="IP cannot be blank!")
        parser.add_argument('area_code', type=str, location='args', required=True, help="area_code cannot be blank!")
        parser.add_argument('area_code_cn', type=str, location='args', required=True, help="area_code_cn cannot be blank!")
        args = parser.parse_args()
        
        try:
            data = servers_schema.load(args)
        except ValidationError as err:
            return err.message, 400

        # print('args:',args)
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO servers (name, ip, area_code, area_code_cn) VALUES (%s, %s, %s, %s)
            """, (data['name'], data['ip'], data['area_code'], data['area_code_cn'],))
        connection.commit()
        new_id = cursor.lastrowid
        cursor.close()
        connection.close()
        return {'id': new_id, 'message': 'insert done'}, 201
