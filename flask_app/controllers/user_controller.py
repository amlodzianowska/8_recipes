from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route("/")
def registration():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    if not User.validate_register(request.form):
        return redirect("/")
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : bcrypt.generate_password_hash(request.form['password'])
    }
    user_id = User.save_user(data)
    session['user_id'] = user_id
    return redirect("/dashboard")

@app.route("/login", methods = ['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect("/")
    user_from_db = User.get_by_email(request.form)
    session['user_id'] = user_from_db.id

    return redirect("/dashboard")

@app.route("/dashboard")
def show_dashboard():
    if "user_id" not in session:
        flash("Please register/login before continuing!")
        return redirect("/")

    data = {
        "user_id" : session['user_id']
    }

    user = User.get_user_by_id(data)
    all_recipes = Recipe.all_recipes_with_cooks()

    return render_template("dashboard.html", user = user, all_recipes=all_recipes)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")