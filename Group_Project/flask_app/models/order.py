from flask import flash
from flask_app import app
from flask_app.models.pizza import Pizza
from flask_app.config.mysqlconnection import connectToMySQL 
from datetime import datetime

db = "Pizza_Time"
class Order:
    def __init__(self,data):
        self.id = data["id"]
        self.name = data["name"]
        self.user_id = data["user_id"]
        self.pizza_id = data["pizza_id"]

    @classmethod
    def save(cls, data):
        pizza = Pizza(data)
        pizza.save()

        query = "INSERT INTO orders (name, created_at, updated_at, user_id, pizza_id) VALUES (%(name)s, NOW(), NOW(), %(user_id)s, %(pizza_id)s);"
        data = {
            'name': data['name'],
            'user_id': data['user_id'],
            'pizza_id': pizza.id,
        }
        order_id = connectToMySQL(db).query_db(query, data)
        return order_id



    @classmethod
    def get_all(cls):
        query = "SELECT * FROM orders;"
        results = connectToMySQL(db).query_db(query)
        orders = []
        for row in results:
            orders.append(row)
        return orders
    
    
    @classmethod
    def get_orders_by_user_id(cls, user_id):
        query = """
                SELECT 
                    pizzas.method, 
                    pizzas.qty, 
                    pizzas.size, 
                    pizzas.crust, 
                    pizzas.toppings 
                FROM 
                    orders 
                    JOIN pizzas ON orders.pizza_id = pizzas.id
                WHERE 
                    orders.user_id = %(user_id)s
                """
        data = {
            "user_id": user_id
        }
        results = connectToMySQL(db).query_db(query, data)
        print("AA")
        orders = []
        for row in results:
            orders.append(row)
        return orders


    
    @classmethod
    def get_by_name(cls,data):
        query = "SELECT * FROM orders WHERE name=%(name)s;"
        results = connectToMySQL(db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])


    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM orders WHERE id=%(id)s;"
        return connectToMySQL(db).query_db(query,data)

