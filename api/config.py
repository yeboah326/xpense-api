import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class BaseConfig(object):
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ERROR_MESSAGE_KEY = os.getenv("JWT_ERROR_MESSAGE_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
