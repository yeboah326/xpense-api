from api.extensions import db
from secrets import token_hex
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "xp_user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(120), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(120), nullable=False)

    @property
    def password(self):
        raise AttributeError("Password is a write-only field")

    @password.setter
    def password(self, password) -> None:
        self.password_hash = generate_password_hash(password)
        self.public_id = token_hex(15)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)
    
    @classmethod
    def find_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def find_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_user_by_public_id(cls, public_id):
        return cls.query.filter_by(public_id=public_id).first()