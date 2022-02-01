from api.extensions import fake
from api.user.models import User
from .setup import create_user, truncate_db


def test_user_register_successful(client):
    # Clear the database
    truncate_db()

    # Generate the data for the test
    data = {
        "email": fake.email(),
        "username": fake.user_name(),
        "password": fake.password()
    }

    # Create the request and store the response
    response = client.post("/api/user/register", json=data)

    # Retrieve the created user
    user = User.find_user_by_email(data["email"])

    assert response.status_code == 201
    assert user
    assert response.json["email"] == data["email"]
    assert response.json["username"] == data["username"]
    assert user.username == data["username"]
    assert user.email == data["email"]

    # Clear the database
    truncate_db()


def test_user_register_validation_error(client):
    # Clear the database
    truncate_db()

    # Generate the data for the test
    data = {
        "email": fake.email(),
        "username": fake.user_name(),
    }

    # Create the request and store the response
    response = client.post("/api/user/register", json=data)

    assert response.status_code == 400
    assert response.json["message"] == "Validation error"
    assert response.json["detail"]["json"]["password"] == [
        'Missing data for required field.'
    ]

    # Clear the database
    truncate_db()


def test_user_login_successful(client):
    # Clear the database
    truncate_db()

    # Create user and return crendentials
    user = create_user(client)["successful"]

    # Create the request to login the user
    response = client.post("/api/user/login", json=user)

    assert response.status_code == 200
    assert response.json['username'] == user["username"]
    assert response.json['token']
    assert response.json['public_id']

    # Clear the database
    truncate_db()


def test_user_login_validation_error(client):
    # Clear the database
    truncate_db()

    # Create user and return crendentials
    user = create_user(client)["validation_error"]

    # Create the request to login the user
    response = client.post("/api/user/login", json=user)

    assert response.status_code == 400
    assert response.json["message"] == "Validation error"
    assert response.json["detail"]["json"]["password"] == [
        'Missing data for required field.'
    ]

    # Clear the database
    truncate_db()


def test_user_login_not_found(client):
    # Clear the database
    truncate_db()

    # Create user and return crendentials
    user = create_user(client)["not_found"]

    # Create the request to login the user
    response = client.post("/api/user/login", json=user)

    assert response.status_code == 404
    assert response.json["message"] == "Invalid credentials"
    assert response.json["detail"] == "A user with the given credentials does not exist"


    # Clear the database
    truncate_db()