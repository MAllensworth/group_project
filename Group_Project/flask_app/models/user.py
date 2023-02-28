from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 



class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.address = data["address"]
        self.city = data["city"]
        self.state = data["state"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.pizzas = []

    @classmethod
    def get_all(cls):
            
        query = "SELECT * FROM users;"

        results = connectToMySQL('pizza_time').query_db(query)

        users = []

        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, address, city, state, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(address)s, %(city)s, %(state)s, %(password)s);"
        return connectToMySQL('pizza_time').query_db(query, data)
    
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('pizza_time').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def select_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
    

        result = connectToMySQL('pizza_time').query_db(query, data)
        print(result)
        if result:
            user = result[0]

            return user

        return False

    @classmethod
    def update(cls, data):
        query = "UPDATE users set first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, address = %(address)s, city = %(city)s, state = %(state)s WHERE id = %(id)s; "
        return connectToMySQL('pizza_time').query_db(query, data)

    @classmethod
    def remove(cls, data):
        query = "DELETE FROM users WHERE id = %(user_id)s;"
        return connectToMySQL('pizza_time').query_db(query, data)


    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('pizza_time').query_db(query, user)
        if len(results) >= 1:
            flash("Email Already Taken", "register")
            is_valid = False

        if len(user['first_name']) < 3:
            flash("First Name Required, Must Be 2 Characters Long", "register")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last Name Required, Must Be 2 Characters Long", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email", "register")
            is_valid = False
        if len(user['address']) < 3:
            flash("Address Needs To Be at Least 3 Characters Long", "register")
            is_valid = False
        if len(user['city']) < 3:
            flash("City Needs To Be at Least 3 Characters Long", "register")
            is_valid = False
        if len(user['state']) < 1:
            flash("Please Select A State", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Please Enter A Valid Password Min of 8 characters & Must Contain at Least One Number &  Must Contain at Least One Uppercase Letter", "register")
            is_valid = False
        elif not any(char.isdigit() for char in user['password'] ) :
            flash("Password Must Contain a Min of 8 characters, at Least One Number & at Least One Uppercase Letter", "register")
            is_valid = False
        elif not any(char.isupper() for char in user['password'] ) :
            flash("Password Must Contain a Min of 8 characters, at Least One Number & at Least One Uppercase Letter", "register")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash ("Passwords Do Not Match", "register")
        return is_valid

    @staticmethod
    def validate_account_update(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('pizza_time').query_db(query, user)
        if len(results) >= 1:
            flash("Email Already Taken")
            is_valid = False

        if len(user['first_name']) < 3:
            flash("First Name Required, Must Be 2 Characters Long")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last Name Required, Must Be 2 Characters Long")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email")
            is_valid = False
        if len(user['address']) < 3:
            flash("Address Needs To Be at Least 3 Characters Long")
            is_valid = False
        if len(user['city']) < 3:
            flash("City Needs To Be at Least 3 Characters Long")
            is_valid = False
        if len(user['state']) < 1:
            flash("Please Select A State" )
            is_valid = False
        return is_valid
