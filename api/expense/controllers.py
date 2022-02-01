from apiflask import APIBlueprint, HTTPError, doc, output, input
from api.extensions import db
from api.generic_schema import GenericResponse
from api.user.models import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from .schema import ExpenseDump, ExpenseLoad, ExpenseMonthSumary, ExpenseSummary
from .models import Expense
from .utils import generate_user_month_summary, generate_user_summary

expense = APIBlueprint("expense", __name__, url_prefix="/api/expense")


@expense.post("/")
@doc(summary="Create an expense",
     description="An endpoint to create a new expense",
     responses=[201, 400, 401])
@input(ExpenseLoad)
@output(ExpenseDump, 201)
@jwt_required()
def expense_new(data):
    # Retrieve the user
    user = User.find_user_by_public_id(get_jwt_identity())

    # Create the expense
    expense = Expense(**data)
    expense.user_id = user.id

    # Save to the database
    db.session.add(expense)
    db.session.commit()

    return expense


@expense.get("/<int:id>")
@doc(summary="Get expense",
     description="An endpoint to get a single expense by id",
     responses=[200, 401, 404])
@output(ExpenseDump, 200)
@jwt_required()
def expense_get_by_id(id):
    # Retrieve the user
    user = User.find_user_by_public_id(get_jwt_identity())

    # Retrieve the expense
    expense = Expense.find_expense_by_id(id=id, user_id=user.id)

    if expense:
        return expense

    raise HTTPError(404,
                    message="Expense not found",
                    detail="The given id does not match an existing expense")


@expense.put("/<int:id>")
@doc(summary="Edit expense",
     description="An endpoint to edit an existing expense",
     responses=[200, 400, 401, 404])
@input(ExpenseLoad)
@output(ExpenseDump, 200)
@jwt_required()
def expense_edit_by_id(id, data):
    # Retrieve the user
    user = User.find_user_by_public_id(get_jwt_identity())

    # Retrieve the expense
    expense = Expense.find_expense_by_id(id=id, user_id=user.id)

    if expense:
        # Modify the expense instance
        for attribute, value in data.items():
            setattr(expense, attribute, value)

        # Save the changes
        db.session.commit()

        return expense

    raise HTTPError(404,
                    message="Expense not found",
                    detail="The given id does not match an existing expense")


@expense.delete("/<int:id>")
@doc(summary="Delete expense",
     description="An endpoint to delete an existing expense",
     responses=[200, 400, 401, 404])
@output(GenericResponse)
@jwt_required()
def expense_delete_by_id(id):
    # Retrieve the user
    user = User.find_user_by_public_id(get_jwt_identity())

    # Retrieve the expense
    expense = Expense.find_expense_by_id(id=id, user_id=user.id)

    if expense:
        # Delte the expense instance
        db.session.delete(expense)
        db.session.commit()

        return {"message": "Expense deleted successfully"}, 200

    raise HTTPError(404,
                    message="Expense not found",
                    detail="The given id does not match an existing expense")


@expense.get("/")
@doc(summary="Get all expenses",
     description="An endpoint to get all expenses",
     responses=[200, 400, 401])
@output(ExpenseDump(many=True), 200)
@jwt_required()
def expense_get_all():
    # Retrieve the user
    user = User.find_user_by_public_id(get_jwt_identity())

    expenses = Expense.find_expenses_by_user_id(user.id)

    return expenses


@expense.get("/summary")
@doc(summary="Get user summary",
     description="An endpoint to get summary of user expenses")
@output(ExpenseSummary, 200)
@jwt_required()
def expense_get_summary():
    # Retrieve the user
    user = User.find_user_by_public_id(get_jwt_identity())

    expense_summary = generate_user_summary(user.id)

    return expense_summary


@expense.get("/month/<int:index>")
@doc(summary="Get all expenses for the month",
     description="An endpoint to get all user expenses for the given month")
@output(ExpenseMonthSumary, 200)
@jwt_required()
def expense_get_month(index):
    # Retrieve the user
    user = User.find_user_by_public_id(get_jwt_identity())

    month_summary = generate_user_month_summary(user.id, index)

    return month_summary