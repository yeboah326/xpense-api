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
        "today": today_sum if today_sum else 0,
        "seven_days": seven_days_sum if seven_days_sum else 0,
        "thirty_days": thirty_days_sum if thirty_days_sum else 0,
        "sixty_days": sixty_days_sum if sixty_days_sum else 0
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

    # This ensures that no value returned is a null value
    expenses_total_sum = expenses_total_sum if expenses_total_sum else 0

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


def generate_user_all_months_summary(user_id):
    # Generate the date for today
    today = datetime.today()

    # Month Expenses
    monthly_expenses = [
        {
            "january": [{
                'days': {},
            }]
        },
        {
            "february": [{
                'days': {},
            }]
        },
        {
            "march": [{
                'days': {},
            }]
        },
        {
            "april": [{
                'days': {},
            }],
        },
        {
            "may": [{
                'days': {},
            }],
        },
        {
            "june": [{
                'days': {},
            }],
        },
        {
            "july": [{
                'days': {},
            }],
        },
        {
            "august": [{
                'days': {},
            }],
        },
        {
            "september": [{
                'days': {},
            }],
        },
        {
            "october": [{
                'days': {},
            }],
        },
        {
            "november": [{
                'days': {},
            }],
        },
        {
            "december": [{
                'days': {},
            }]
        },
    ]

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

    for month in range(1, 13):

        expenses_list = []

        for day in range(1, 32):
            expenses = db.session.query(Expense).filter(
                Expense.user_id == user_id).filter(
                    extract("month", Expense.date) == month).filter(
                        extract("year", Expense.date) == today.year).filter(
                            extract("day", Expense.date) == day).all()
            if expenses:
                expenses_list.append({f"{day}":expenses})

        # Add all the expenses for the current month
        monthly_expenses[month - 1][months[month]][0]['days'] = expenses_list

        # Compute the sum for the month
        expenses_total_sum = db.session.query(
            func.sum(Expense.amount).filter(Expense.user_id == user_id).filter(
                extract("month", Expense.date) == month).filter(
                    extract("year", Expense.date) == today.year)).first()[0]

        # This ensures that no value returned is a null value
        expenses_total_sum = expenses_total_sum if expenses_total_sum else 0

        # Add the sum of the expenses for the current month
        monthly_expenses[month - 1][
            months[month]][0]['total_amount'] = expenses_total_sum

        # Add the year to the returned values
        monthly_expenses[month - 1][months[month]][0]['year'] = today.year

        # Add the month index
        monthly_expenses[month - 1][months[month]][0]['month_index'] = month

        # Add the name of the month again
        monthly_expenses[month - 1][months[month]][0]['month'] = months[month]

    return {"all_expenses": monthly_expenses}
