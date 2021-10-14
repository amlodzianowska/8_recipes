from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash
from flask_app.models import user


class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.made_on = data['made_on']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

        self.cook = {}

    @staticmethod
    def validate_recipe(form_data):
        is_valid = True

        if form_data['name'] == "":
            flash("Please enter a valid name!")
            is_valid = False

        elif len(form_data['name']) < 3:
            flash("Name must be at least 3 characters long!")
            is_valid = False

        if form_data['description'] == "":
            flash("Please enter a valid description!")
            is_valid = False

        elif len(form_data['description']) < 3:
            flash("Description must be at least 3 characters long!")
            is_valid = False

        if form_data['instructions'] == "":
            flash("Please enter valid instructions!")
            is_valid = False

        elif len(form_data['instructions']) < 3:
            flash("Instructions must be at least 3 characters long!")
            is_valid = False

        if form_data['made_on'] == "":
            flash("Please enter valid date!")
            is_valid = False

        return is_valid

    @classmethod
    def save_recipe(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, made_on, under_30, user_id, created_at, updated_at) VALUES(%(name)s, %(description)s, %(instructions)s, %(made_on)s, %(under_30)s, %(user_id)s, NOW(), NOW());"
        results = connectToMySQL("recipes").query_db(query, data)
        return results

    @classmethod
    def all_recipes_with_cooks(cls):
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id;"
        results = connectToMySQL("recipes").query_db(query)
        all_recipes = []
        for row in results:
            one_recipe = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at'],
            }
            one_recipe.cook = user.User(user_data)
            all_recipes.append(one_recipe)
        return all_recipes
    
    @classmethod
    def get_recipe_with_cook(cls, data):
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(recipe_id)s;"
        results = connectToMySQL("recipes").query_db(query, data)
        recipe = cls(results[0])
        user_data = {
            "id": results[0]['users.id'],
            "first_name": results[0]['first_name'],
            "last_name": results[0]['last_name'],
            "email": results[0]['email'],
            "password": results[0]['password'],
            "created_at": results[0]['users.created_at'],
            "updated_at": results[0]['users.updated_at'],
        }
        recipe.cook = user.User(user_data)
        return recipe

    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, made_on = %(made_on)s, under_30 = %(under_30)s, updated_at = NOW() WHERE id = %(recipe_id)s;"
        results = connectToMySQL("recipes").query_db(query, data)
        return
    
    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(recipe_id)s"
        results = connectToMySQL("recipes").query_db(query, data)
        return