from apiflask import Schema
from apiflask.fields import DateTime, String, Integer


class ExpenseLoad(Schema):
    amount = Integer(required=True)
    description = String(required=True)
    date = DateTime(required=True)
    user_id = String(required=True)


class ExpenseDump(Schema):
    id = Integer(required=True)
    amount = Integer(required=True)
    description = String(required=True)
    date = DateTime(required=True)
    user_id = String(required=True)
