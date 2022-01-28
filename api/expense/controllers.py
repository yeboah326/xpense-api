from apiflask import APIBlueprint, doc, output, input
from .schema import ExpenseDump, ExpenseLoad

expense = APIBlueprint("expense", __name__, url_prefix="/api/expense")


@expense.post("/")
@doc(summary="Create an expense",
     description="An endpoint to create a new expense")
@input(ExpenseLoad)
@output(ExpenseDump)
def expense_new():
    return {"message":"hello"}, 200


@expense.get("/<int:id>")
@doc(summary="Get expense",
     description="An endpoint to get a single expense by id")
def expense_get_by_id(id):
    pass


@expense.put("/<int:id>")
@doc(summary="Edit expense",
     description="An endpoint to edit an existing expense")
def expense_edit_by_id(id):
    pass


@expense.delete("/<int:id>")
@doc(summary="Delete expense",
     description="An endpoint to delete an existing expense")
def expense_delete_by_id(id):
    pass


@expense.get("/")
@doc(summary="Get all expenses", description="An endpoint to get all expenses")
def expense_get_all():
    pass


@expense.get("/summary")
@doc(summary="Get user summary",
     description="An endpoint to get summary of user expenses")
def expense_get_summary():
    pass


@expense.get("/month<int:index>")
@doc(summary="Get all expenses for the month",
     description="An endpoint to get all user expenses for the given month")
def expense_get_month(index):
    pass