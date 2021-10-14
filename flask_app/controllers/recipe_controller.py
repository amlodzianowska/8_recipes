from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.recipe import Recipe
from flask_app.models.user import User

@app.route("/new_recipe")
def new_recipe():

    if "user_id" not in session:
        flash("Please register/login before continuing!")
        return redirect("/")

    data = {
        "user_id" : session['user_id']
    }

    user = User.get_user_by_id(data)

    return render_template("new_recipe.html", user=user)

@app.route("/add_recipe", methods = ['POST'])
def add_recipe():

    if not Recipe.validate_recipe(request.form):
        return redirect("/new_recipe")

    data = {
        "name" : request.form['name'],
        "description" : request.form['description'],
        "instructions" : request.form['instructions'],
        "made_on" : request.form['made_on'],
        "under_30" : request.form['under_30'],
        "user_id" : request.form['user_id']
    }
    Recipe.save_recipe(data)

    return redirect("/dashboard")

@app.route("/show/<int:recipe_id>")
def show_recipe(recipe_id):
    if "user_id" not in session:
        flash("Please register/login before continuing!")
        return redirect("/")
    data = {
        "recipe_id" : recipe_id
    }

    recipe = Recipe.get_recipe_with_cook(data)

    return render_template("show_recipe.html", recipe=recipe)

@app.route("/edit/<int:recipe_id>")
def edit_recipe(recipe_id):
    if "user_id" not in session:
        flash("Please register/login before continuing!")
        return redirect("/")
    data = {
        "recipe_id" : recipe_id
    }
    recipe = Recipe.get_recipe_with_cook(data)

    return render_template("edit_recipe.html", recipe=recipe)

@app.route("/update_recipe/<int:recipe_id>", methods = ['POST'])
def update_recipe(recipe_id):
    if not Recipe.validate_recipe(request.form):
        return redirect(f"/edit/{recipe_id}")
    data = {
        "name" : request.form['name'],
        "description" : request.form['description'],
        "instructions" : request.form['instructions'],
        "made_on" : request.form['made_on'],
        "under_30" : request.form['under_30'],
        "recipe_id" : recipe_id
    }

    Recipe.update_recipe(data)

    return redirect("/dashboard")

@app.route("/delete/<int:recipe_id>")
def delete_recipe(recipe_id):
    data = {
        "recipe_id" : recipe_id
    }
    Recipe.delete_recipe(data)

    return redirect("/dashboard")