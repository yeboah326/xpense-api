from random import random
from api.extensions import fake
from api.expense.models import Expense
from .setup import create_expense, create_expenses, login_user, truncate_db


def test_expense_new_successful(client):
    truncate_db()

    user = login_user(client)

    data = {
        "amount": abs(round(fake.pyint() * random(), 2)),
        "description": fake.sentence(),
        "date": fake.date_this_month().isoformat()
    }

    response = client.post(
        "/api/expense/",
        json=data,
        headers={"Authorization": f"Bearer {user['token']}"})

    expense = Expense.query.filter_by(amount=data["amount"],
                                      description=data["description"]).first()

    assert response.status_code == 201
    assert expense
    assert response.json["amount"] == data["amount"]
    assert response.json["description"] == data["description"]
    assert response.json["date"] == data["date"]

    truncate_db()


def test_expense_new_validation_error(client):
    truncate_db()

    user = login_user(client)

    data = {
        "description": fake.sentence(),
        "date": fake.date_this_month().isoformat()
    }

    response = client.post(
        "/api/expense/",
        json=data,
        headers={"Authorization": f"Bearer {user['token']}"})

    assert response.status_code == 400
    assert response.json["detail"]["json"]["amount"] == [
        "Missing data for required field."
    ]
    assert response.json["message"] == "Validation error"

    truncate_db()


def test_expense_new_unauthorized(client):
    truncate_db()

    user = login_user(client)

    data = {
        "amount": abs(round(fake.pyint() * random(), 2)),
        "description": fake.sentence(),
        "date": fake.date_this_month().isoformat()
    }

    response = client.post("/api/expense/", json=data)

    assert response.status_code == 401
    assert response.json["message"] == "Missing Authorization Header"

    truncate_db()


def test_expense_get_by_id_successful(client):
    truncate_db()

    expense = create_expense(client)

    response = client.get(
        f"/api/expense/{expense['expense']['id']}",
        headers={"Authorization": f"Bearer {expense['user']['token']}"})

    assert response.status_code == 200
    assert response.json["amount"] == expense["expense"]["amount"]
    assert response.json["description"] == expense["expense"]["description"]
    assert response.json["date"] == expense["expense"]["date"]

    truncate_db()


def test_expense_get_by_id_unauthorized(client):
    truncate_db()

    expense = create_expense(client)

    response = client.get(f"/api/expense/{expense['expense']['id']}")

    assert response.status_code == 401
    assert response.json["message"] == "Missing Authorization Header"

    truncate_db()


def test_expense_get_by_id_not_found(client):
    truncate_db()

    expense = create_expense(client)

    response = client.get(
        f"/api/expense/{expense['expense']['id'] + 1}",
        headers={"Authorization": f"Bearer {expense['user']['token']}"})

    assert response.status_code == 404
    assert response.json[
        "detail"] == "The given id does not match an existing expense"
    assert response.json["message"] == "Expense not found"

    truncate_db()


def test_expense_edit_by_id_successful(client):
    truncate_db()

    expense = create_expense(client)

    data = {
        "amount": abs(round(fake.pyint() * random(), 2)),
        "description": fake.sentence(),
        "date": fake.date_this_month().isoformat()
    }

    response = client.put(
        f"/api/expense/{expense['expense']['id']}",
        json=data,
        headers={"Authorization": f"Bearer {expense['user']['token']}"})

    modified_expense = Expense.query.filter_by(amount=data["amount"],
                                               description=data["description"])

    assert response.status_code == 200
    assert response.json["amount"] == data["amount"]
    assert response.json["description"] == data["description"]
    assert response.json["date"] == data["date"]

    truncate_db()


def test_expense_edit_by_id_validation_error(client):
    truncate_db()

    expense = create_expense(client)

    data = {
        "description": fake.sentence(),
        "date": fake.date_this_month().isoformat()
    }

    response = client.put(
        f"/api/expense/{expense['expense']['id']}",
        json=data,
        headers={"Authorization": f"Bearer {expense['user']['token']}"})

    assert response.status_code == 400
    assert response.json['detail']['json']['amount'] == [
        'Missing data for required field.'
    ]
    assert response.json['message'] == 'Validation error'

    truncate_db()


def test_expense_edit_by_id_unauthorized(client):
    truncate_db()

    expense = create_expense(client)

    data = {
        "amount": abs(round(fake.pyint() * random(), 2)),
        "description": fake.sentence(),
        "date": fake.date_this_month().isoformat()
    }

    response = client.put(f"/api/expense/{expense['expense']['id']}",
                          json=data)

    assert response.status_code == 401
    assert response.json["message"] == "Missing Authorization Header"

    truncate_db()


def test_expense_edit_by_id_not_found(client):
    truncate_db()

    expense = create_expense(client)

    data = {
        "amount": abs(round(fake.pyint() * random(), 2)),
        "description": fake.sentence(),
        "date": fake.date_this_month().isoformat()
    }

    response = client.put(
        f"/api/expense/{expense['expense']['id'] + 1}",
        json=data,
        headers={"Authorization": f"Bearer {expense['user']['token']}"})

    assert response.status_code == 404
    assert response.json[
        'detail'] == "The given id does not match an existing expense"
    assert response.json['message'] == "Expense not found"

    truncate_db()


def test_expense_delete_by_id_successful(client):
    truncate_db()

    expense = create_expense(client)

    response = client.delete(
        f"api/expense/{expense['expense']['id']}",
        headers={"Authorization": f"Bearer {expense['user']['token']}"})

    deleted_expense = Expense.query.filter_by(
        amount=expense["expense"]["amount"],
        description=expense["expense"]["description"]).first()

    assert response.status_code == 200
    assert response.json["message"] == "Expense deleted successfully"
    assert deleted_expense == None

    truncate_db()


def test_expense_delete_by_id_unauthorized(client):
    truncate_db()

    expense = create_expense(client)

    response = client.delete(f"api/expense/{expense['expense']['id']}")

    assert response.status_code == 401
    assert response.json["message"] == "Missing Authorization Header"

    truncate_db()


def test_expense_delete_by_id_not_found(client):
    truncate_db()

    expense = create_expense(client)

    response = client.delete(
        f"api/expense/{expense['expense']['id'] + 1}",
        headers={"Authorization": f"Bearer {expense['user']['token']}"})

    assert response.status_code == 404
    assert response.json[
        "detail"] == "The given id does not match an existing expense"
    assert response.json["message"] == "Expense not found"

    truncate_db()


def test_expense_get_all_successful(client):
    truncate_db()

    expenses = create_expenses(client)

    response = client.get(
        "/api/expense/",
        headers={"Authorization": f"Bearer {expenses['user']['token']}"})

    assert response.status_code == 200
    assert len(response.json) == 5
    assert response.json[0]['id'] == expenses["expenses"][0].id
    assert response.json[1]['id'] == expenses["expenses"][1].id
    assert response.json[2]['id'] == expenses["expenses"][2].id
    assert response.json[3]['id'] == expenses["expenses"][3].id
    assert response.json[4]['id'] == expenses["expenses"][4].id

    truncate_db()


def test_expense_get_all_unauthorized(client):
    truncate_db()

    expenses = create_expenses(client)

    response = client.get("/api/expense/")

    assert response.status_code == 401
    assert response.json["message"] == "Missing Authorization Header"

    truncate_db()


def test_expense_get_summary(client):
    truncate_db()

    expenses = create_expenses(client)

    response = client.get(
        "/api/expense/summary",
        headers={"Authorization": f"Bearer {expenses['user']['token']}"})

    assert response.status_code == 200
    assert response.json['today']
    assert response.json['seven_days']
    assert response.json['thirty_days']
    assert response.json['sixty_days']

    truncate_db()


def test_expense_get_month(client):
    truncate_db()

    expenses = create_expenses(client)

    response = client.get(
        "/api/expense/month/2",
        headers={"Authorization": f"Bearer {expenses['user']['token']}"})

    assert response.status_code == 200
    assert len(response.json["expenses"])
    assert response.json["expenses_total_sum"]

    truncate_db()