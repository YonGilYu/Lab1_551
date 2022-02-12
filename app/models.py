from flask_restful import abort
from werkzeug.security import check_password_hash, generate_password_hash

from db import db

class IdMixin(db.Model):
    __abstract__ = True

    id = db.Column(
        db.Integer,
        primary_key=True,
        unique=True,
        autoincrement=True,
        nullable=False,
    )

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception:
            abort(http_status_code=400, message={"message": "Something went wrong"})


class User(IdMixin):
    __tablename__ = "users"

    username = db.Column(
        db.String(length=50), unique=True, nullable=False
    )
    psw = db.Column(db.String(length=256), nullable=False)

    def __repr__(self) -> str:
        return f"<Username: {self.username}>"

    @classmethod
    def find_by_username(cls, username: str):
        return cls.query.filter_by(username=username).first()

    def set_password(self, password: str):
        self.psw = generate_password_hash(password=password)

    def check_password(self, password):
        return check_password_hash(pwhash=self.psw, password=password)

class Books_list(IdMixin):
    __tablename__="books_list"

    isbn= db.Column(
        db.String(length=256), unique=True, nullable=False
    )
    title= db.Column(
        db.String(length=256), unique=True, nullable=False
    )
    author= db.Column(
        db.String(length=256), unique=True, nullable=False
    )

    @classmethod
    def find_by_type(cls, isbn: str):
        return cls.query.filter_by(isbn=isbn).first()

