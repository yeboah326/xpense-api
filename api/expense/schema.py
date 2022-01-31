from apiflask import Schema
from apiflask.fields import Date, String, Integer, Float, List, Nested


class ExpenseLoad(Schema):
    amount = Float(required=True)
    description = String(required=True)
    date = Date(required=True)


class ExpenseDump(Schema):
    id = Integer(required=True)
    amount = Float(required=True)
    description = String(required=True)
    date = Date(required=True)
    user_id = Integer(required=True)

class ExpenseSummary(Schema):
    today = Float(required=True)
    seven_days = Float(required=True)
    thirty_day = Float(required=True)
    sixy_days = Float(required=True)

class ExpenseMonthSumary(Schema):
    expenses = List(Nested(ExpenseDump),required=True)
    expense_total_sum = Float(required=True)