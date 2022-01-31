from apiflask import Schema
from apiflask.fields import Email, String


class UserNewLoad(Schema):
    email = Email(required=True)
    username = String(required=True)
    password = String(required=True)


class UserNewDump(Schema):
    public_id = String(required=True)
    email = Email(required=True)
    username = String(required=True)

class UserLoginLoad(Schema):
    username = String(required=True)
    password = String(required=True)

class UserLoginDump(Schema):
    public_id = String(required=True)
    email = Email(required=True)
    username = String(required=True)
    token = String(required=True)
