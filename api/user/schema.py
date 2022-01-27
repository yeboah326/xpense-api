from marshmallow import Schema, fields


class User(Schema):
    public_id = fields.Str(required=True, dump_only=True)
    email = fields.Email(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    token = fields.Str(required=True, dump_only=True)


user_load = User(unknown="EXCLUDE", load_only=True)
user_dump = User(unknown="EXCLUDE", dump_only=True)