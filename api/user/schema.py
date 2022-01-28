from apiflask import Schema
from apiflask.fields import Email, String


class UserLoad(Schema):
    email = Email(required=True)
    username = String(required=True)
    password = String(required=True)


class UserDump(Schema):
    public_Id = String(required=True)
    email = Email(required=True)
    username = String(required=True)
    token = String(required=True)
