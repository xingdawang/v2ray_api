from marshmallow import Schema, fields

# class DataSchema(Schema):
#     ip = fields.String()
#     area = fields.String()
#     config_url = fields.String()
#     record_date = fields.DateTime(format='%Y-%m-%d %H:%M:%S')

class ServersSchema(Schema):
    name = fields.String()
    ip = fields.String()
    area_code = fields.String()
    area_code_cn = fields.String()
    record_date = fields.DateTime(format='%Y-%m-%d')

# data_schema = DataSchema()
servers_schema = ServersSchema()
servers_list_schema = ServersSchema(many=True)