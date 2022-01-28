from apiflask import APIBlueprint, doc

user = APIBlueprint("user", __name__, url_prefix="/api/user")


@user.post("/register")
@doc(summary="Create a new user", description="An endpoint to register a new user")
def user_register():
    pass

@user.post("/login")
@doc(summary="Login user", description="An endpoint to generate a token for an existing user")
def user_login():
    pass

