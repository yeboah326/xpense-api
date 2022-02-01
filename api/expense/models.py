from api.extensions import db
import datetime


class Expense(db.Model):
    __tablename__ = "xp_expense"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Numeric(6,2), nullable=False)
    description = db.Column(db.String(100), nullable=True)
    date = db.Column(db.Date(),
                     default=datetime.datetime.now(),
                     nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("xp_user.id", ondelete="cascade"),
                        nullable=False)

    @classmethod
    def find_expense_by_id(cls, id, user_id):
        return cls.query.filter_by(id=id, user_id=user_id).first()

    @classmethod
    def find_expenses_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()