from marshmallow import fields, Schema


class Expense(Schema):
    id = fields.Int(required=True, dump_only=True)
    amount = fields.Int(required=True)
    description = fields.Str(required=True)
    date = fields.DateTime(required=True)
    user_id = fields.Str(required=True, dump_only=True)


expense_load = Expense(unknown="EXCLUDE", load_only=True)
expense_dump = Expense(unknown="EXCLUDE", dump_only=True)
expense_dump_many = Expense(unknown="EXCLUDE", many=True)