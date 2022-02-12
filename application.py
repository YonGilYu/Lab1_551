from flask import Flask, render_template, request
from flask_restful import Api

from app.models import Books_list, User
from db import db, init_db

import requests
import json

app = Flask(__name__)
api = Api(app=app)

app.config["FLASK_APP"] = "application.py"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/signin")
def signin():
    return render_template("signin.html")


@app.route("/registration")
def registration():
    return render_template("registration.html")


@app.route("/users", methods=["POST"])
def users():
    username: str = request.form.get("username")
    psw: str = request.form.get("psw")
    new_user = User(username=username)
    new_user.set_password(password=psw)
    db.session.add(new_user)
    db.session.commit()
    return render_template("signin.html")


@app.route("/login", methods=["POST"])
def login():
    username: str = request.form.get("username")
    psw: str = request.form.get("psw")
    current_user = User.find_by_username(username=username)
    if not current_user:
        return render_template("error.html")
    if current_user.check_password(password=psw):
        return render_template("home.html")
    return render_template("error.html")


@app.route("/result", methods=["POST"])
def search():
    isbn: str = request.form.get("isbn")
    current_isbn= Books_list.find_by_type(isbn=isbn)
    res= requests.get("https://www.googleapis.com/books/v1/volumes", params={"q": current_isbn})
    print(res.json())
    if not current_isbn:
        return render_template("error.html")
    if current_isbn:
        return render_template("result.html", res=res.json())
    return render_template("error.html")


@app.route("/home", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/logout")
def logout():
    return render_template("/index.html")


@app.before_first_request
def create_tables():
    db.create_all()


def create_app(flask_app):
    init_db(app=flask_app)
    flask_app.run(debug=True)


if __name__ == "__main__":
    create_app(flask_app=app)
