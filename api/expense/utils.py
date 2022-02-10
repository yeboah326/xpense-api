from calendar import month
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

    # List to store the expenses according to days
    expenses_list = []

    for i in range(1, 32):
        expenses = db.session.query(Expense).filter(
            Expense.user_id == user_id).filter(
                extract("month", Expense.date) == index).filter(
                    extract("year", Expense.date) == today.year).filter(
                        extract("day", Expense.date) == i).all()
        if expenses:
            expenses_list.append({f"{i}": expenses})

    expenses_total_sum = db.session.query(
        func.sum(Expense.amount).filter(Expense.user_id == user_id).filter(
            extract("month", Expense.date) == index).filter(
                extract("year", Expense.date) == today.year)).first()[0]

    months = {
        1: "january",
        2: "february",
        3: "march",
        4: "april",
        5: "may",
        6: "june",
        7: "july",
        8: "august",
        9: "september",
        10: "october",
        11: "november",
        12: "december",
    }

    return {
        "expenses": expenses_list,
        "expenses_total_sum": expenses_total_sum,
        'month': months[index],
        'month_index': index,
        'year': today.year
    }
