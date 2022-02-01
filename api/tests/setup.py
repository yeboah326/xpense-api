from api.extensions import db, fake
from api.expense.models import Expense
from random import random


def truncate_db():
    meta = db.metadata
    for table in meta.sorted_tables[::-1]:
        db.session.execute(table.delete())
    db.session.commit()


def create_user(client):
    # Generate the data
    data = {
        "email": fake.email(),
        "username": fake.user_name(),
        "password": fake.password()
    }

    response = client.post("/api/user/register", json=data)

    return {
        "successful": {
            "username": data["username"],
            "password": data["password"]
        },
        "validation_error": {
            "username": data["username"]
        },
        "not_found": {
            "username": fake.user_name(),
            "password": fake.password()
        }
    }


def login_user(client):
    # Create a user
    user = create_user(client)["successful"]

    # Create the request to login the user
    response = client.post("/api/user/login", json=user)

    return response.json


def create_expense(client):
    # Create a user and login
    user = login_user(client)

    data = {
        "amount": abs(round(fake.pyint() * random(), 2)),
        "description": fake.sentence(),
        "date": fake.date_this_month().isoformat()
    }

    # Create the request and store the response
    response = client.post(
        "/api/expense/",
        json=data,
        headers={"Authorization": f"Bearer {user['token']}"})

    return {"expense": response.json, "user": user}


def create_expenses(client):
    user = login_user(client)

    for i in range(5):
        client.post("/api/expense/",
                    json={
                        "amount": abs(round(fake.pyint() * random(), 2)),
                        "description": fake.sentence(),
                        "date": fake.date_this_month().isoformat()
                    },
                    headers={"Authorization": f"Bearer {user['token']}"})

    return {"expenses": Expense.query.all(), "user": user}
