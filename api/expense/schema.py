from apiflask import Schema
from apiflask.fields import Date, String, Integer, Float, List, Nested, Dict, Mapping, Raw


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
    expenses = List(
        Dict(keys=String,
             values=List(Nested(ExpenseDump), required=True),
             required=True))
    expenses_total_sum = Float(required=True)
    month = String(required=True)
    month_index = Integer(required=True)
    year = Integer(required=True)


class ExpenseDaysArray(Schema):
    day = Dict(key=String, values=List(Nested(ExpenseDump)))


class ExpenseAllMonthsSingleMonth(Schema):
    total_amount = Float(required=True)
    days = List(
        Dict(keys=String,
             values=List(Nested(ExpenseDump), required=True),
             required=True))
    year = Integer(required=True)
    month_index = Integer(required=True)
    month = String(required=True)


# class ExpenseAllMonthsMonth(Schema):
#     all_expenses = Dict(key=String, values=ExpenseAllMonthsSingleMonth)


class ExpenseAllMonthsSummary(Schema):
    january = List(Nested(ExpenseAllMonthsSingleMonth))
    february = List(Nested(ExpenseAllMonthsSingleMonth))
    march = List(Nested(ExpenseAllMonthsSingleMonth))
    april = List(Nested(ExpenseAllMonthsSingleMonth))
    may = List(Nested(ExpenseAllMonthsSingleMonth))
    june = List(Nested(ExpenseAllMonthsSingleMonth))
    july = List(Nested(ExpenseAllMonthsSingleMonth))
    august = List(Nested(ExpenseAllMonthsSingleMonth))
    september = List(Nested(ExpenseAllMonthsSingleMonth))
    october = List(Nested(ExpenseAllMonthsSingleMonth))
    november = List(Nested(ExpenseAllMonthsSingleMonth))
    december = List(Nested(ExpenseAllMonthsSingleMonth))


class ExpenseAll(Schema):
    all_expenses = List(Nested(ExpenseAllMonthsSummary))