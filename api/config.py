import os


class BaseConfig(object):
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ERROR_MESSAGE_KEY = os.getenv("JWT_ERROR_MESSAGE_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")