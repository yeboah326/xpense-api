from api.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "xp_user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(120), )
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(120), nullable=False)

    @property
    def password(self):
        raise AttributeError("Password is a write-only field")

    @password.setter
    def password(self, password) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)