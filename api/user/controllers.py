from apiflask import APIBlueprint, HTTPError, doc, input, output
from api.extensions import db
from api.user.schema import UserLoginDump, UserLoginLoad, UserNewDump, UserNewLoad
from flask_jwt_extended import create_access_token
from .models import User

user = APIBlueprint("user", __name__, url_prefix="/api/user")


@user.post("/register")
@input(UserNewLoad)
@output(UserNewDump, 201)
@doc(summary="Create a new user",
     description="An endpoint to register a new user")
def user_register(data):
    user = User(**data)

    # Add to the database
    db.session.add(user)
    db.session.commit()

    return user


@user.post("/login")
@input(UserLoginLoad)
@output(UserLoginDump, 200)
@doc(summary="Login user",
     description="An endpoint to generate a token for an existing user",
     responses=[200, 400, 404])
def user_login(data):
    user = User.find_user_by_username(data["username"])

    if user:
        correct_password = user.check_password(data["password"])
        if correct_password:
            user.token = create_access_token(identity=user.public_id)
            return user
        raise HTTPError(
            400,
            message="Invalid credentials",
            detail="Either the username or password provided is wrong")

    raise HTTPError(404,
                    message="Invalid credentials",
                    detail="A user with the given credentials does not exist")
