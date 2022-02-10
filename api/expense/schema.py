from apiflask import Schema
from apiflask.fields import Date, String, Integer, Float, List, Nested, Dict


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
    thirty_days = Float(required=True)
    sixty_days = Float(required=True)


class ExpenseMonthSumary(Schema):
    expenses = List(Dict(keys=String, values=List(Nested(ExpenseDump), required=True), required=True))
    expenses_total_sum = Float(required=True)
    month = String(required=True)
    month_index = Integer(required=True)
    year = Integer(required=True)


class ExpenseDay(Schema):
    day = Integer(required=True)