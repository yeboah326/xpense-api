import os
from dotenv import load_dotenv
import datetime

# Load environment variables
load_dotenv()


class BaseConfig(object):
    JWT_ACCESS_TOKEN_EXPIRES=datetime.timedelta(hours=3)
    JWT_ERROR_MESSAGE_KEY = os.getenv("JWT_ERROR_MESSAGE_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
