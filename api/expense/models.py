from api.extensions import db
import datetime


class Expense(db.Model):
    __tablename__ = "xp_expense"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(100), nullable=True)
    date = db.Column(db.DateTime(),
                     default=datetime.datetime.now(),
                     nullable=False)
    user_id = db.Column(db.Integer)
