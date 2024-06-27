from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from ..utils.db import get_db_connection

class OperatorResource(Resource):

    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('phone_or_email', type=str, location='args', required=True, help='Phone or email are required')
        parser.add_argument('password', type=str, location='args', required=True, help='Password is required')
        args = parser.parse_args()
        phone_or_email = args['phone_or_email']
        password = args['password']

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Check if the user exists by phone or email
        cursor.execute("""
            SELECT * FROM operators 
            WHERE (phone = %s OR email = %s)
        """, (phone_or_email, phone_or_email))
        user = cursor.fetchone()

        cursor.close()
        connection.close()

        # NOTE:
        # when generating user password, please use: generate_password_hash(password)

        if user and check_password_hash(user['password'], password):
            access_token = create_access_token(identity=phone_or_email)
            refresh_token = create_refresh_token(identity=phone_or_email)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"message": "Invalid credentials"}, 401