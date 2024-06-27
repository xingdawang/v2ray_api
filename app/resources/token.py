from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_restful import Resource

class TokenResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        return {"access_token": new_access_token}, 200
