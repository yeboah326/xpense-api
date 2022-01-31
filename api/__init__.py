from apiflask import APIFlask

from api.config import BaseConfig
from .extensions import *
from dotenv import load_dotenv
from .user.controllers import user
from .expense.controllers import expense

# Load environment variables
load_dotenv()


def create_app():
    app = APIFlask(__name__, title="xpense API", version="1.0.0")

    # Flask application configurations
    app.config.from_object(BaseConfig)

    # Flask application extensions
    db.init_app(app)
    cors.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(user)
    app.register_blueprint(expense)

    return app