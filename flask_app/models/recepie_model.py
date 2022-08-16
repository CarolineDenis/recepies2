from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user_model 
from flask_app import DATABASE
from flask import flash
import re

class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date = data['date']
        self.under_30_min = data['under_30_min']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO recepies (name,description,instructions,date,under_30_min,user_id, created_at, updated_at) VALUES (%(name)s,%(description)s,%(instructions)s,%(date)s,%(under_30_min)s,%(user_id)s,NOW(),NOW())"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def get_all(cls,data):
        query = "SELECT * FROM recepies JOIN users ON users.id = recepies.user_id;"
        results =  connectToMySQL(DATABASE).query_db(query,data)
        list_recepies =[]
        for b in results:
            this_recepie = cls(b)
            user_data = {
                **b,
                'id': b['users.id'],
                'created_at': b['users.created_at'],
                'updated_at': b['users.updated_at']
            }
            this_user = user_model.User(user_data)
            this_recepie.author = this_user
            list_recepies.append(this_recepie)
        return list_recepies

    @classmethod
    def read_one(cls, data): 
        query = "SELECT * FROM recepies LEFT JOIN users ON users.id = recepies.user_id WHERE recepies.id=%(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        row = results[0]
        this_recipe = cls(row)
        data={
            **row,
            'id': row['users.id'],
            'created_at': row['users.created_at'],
            'updated_at': row['users.updated_at']
        }
        this_author = user_model.User(data)
        this_recipe.author = this_author
        return this_recipe

    @classmethod
    def udpdate(cls, data):
        query = "UPDATE recepies SET name = %(name)s, description = %(description)s, instructions = %(instructions)s,date = %(date)s,under_30_min = %(under_30_min)s" \
            "WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recepies WHERE id= %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @staticmethod
    def validate_form(form):
        is_valid = True
        if len(form['name']) < 3:
            flash("Name must be at least 3 characters.", "err_name")
            is_valid = False
        if len(form['description']) < 3:
            flash("Description must be at least 3 characters.", "err_description")
            is_valid = False
        if len(form['instructions']) < 3:
            flash("Instructions must be at least 3 characters.", "err_instructions")
            is_valid = False
        if len(form['date']) < 1:
            flash("Date must be chose", "err_date")
            is_valid = False
        if "under_30_min" not in form:
            flash("Under 30 minutes needs to be specified", "err_under_30_min")
            is_valid = False
        return is_valid
