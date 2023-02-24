from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_app import app
from flask_bcrypt import Bcrypt
from flask import render_template, request, redirect, session, flash

bcrypt = Bcrypt(app)

@app.route("/")
def log_and_reg():
    return render_template("index.html")