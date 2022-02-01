from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from faker import Faker

db = SQLAlchemy()
cors = CORS()
jwt = JWTManager()
migrate = Migrate()
fake = Faker()