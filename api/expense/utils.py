from datetime import datetime, timedelta
from api.expense.models import Expense
from api.extensions import db
from sqlalchemy import func, extract


def generate_user_summary(user_id):
    # Generate the date for today
    today = datetime.today().date()
    seven_days = today - timedelta(days=6)
    thirty_days = today - timedelta(days=29)
    sixty_days = today - timedelta(days=59)

    # Generate summaries
    today_sum = db.session.query(
        func.sum(Expense.amount).filter(Expense.user_id == user_id).filter(
            Expense.date == today)).first()[0]
    seven_days_sum = db.session.query(
        func.sum(Expense.amount).filter(Expense.user_id == user_id).filter(
            Expense.date >= seven_days)).first()[0]
    thirty_days_sum = db.session.query(
        func.sum(Expense.amount).filter(Expense.user_id == user_id).filter(
            Expense.date >= thirty_days)).first()[0]
    sixty_days_sum = db.session.query(
        func.sum(Expense.amount).filter(Expense.user_id == user_id).filter(
            Expense.date >= sixty_days)).first()[0]

    return {
        "today": today_sum,
        "seven_days": seven_days_sum,
        "thirty_days": thirty_days_sum,
        "sixty_days": sixty_days_sum
    }


def generate_user_month_summary(user_id, index):
    # Generate the date for today
    today = datetime.today()

    expenses = db.session.query(Expense).filter(
        Expense.user_id == user_id).filter(
            extract("month", Expense.date) == index).filter(
                extract("year", Expense.date) == today.year).all()

    expenses_total_sum = db.session.query(
        func.sum(Expense.amount).filter(Expense.user_id == user_id).filter(
            extract("month", Expense.date) == index).filter(
                extract("year", Expense.date) == today.year)).first()[0]

    return {"expenses": expenses, "expenses_total_sum": expenses_total_sum}
