from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask_app.models import order
from flask import flash

db = "Pizza_Time"
class Pizza:
    def __init__(self, data):
        self.id = data.get('id')
        self.method = data['method']
        self.size = data['size']
        self.toppings = data['toppings']
        self.crust = data['crust']
        self.qty = data['qty']

    def save(self):
        query = "INSERT INTO pizzas (method, size, toppings, crust, qty, created_at, updated_at) VALUES (%(method)s, %(size)s, %(toppings)s, %(crust)s, %(qty)s, NOW(), NOW());"

        data = {
            'method': self.method,
            'size': self.size,
            'toppings': self.toppings,
            'crust': self.crust,
            'qty': self.qty,
        }
        pizza_id = connectToMySQL(db).query_db(query, data)
        self.id = pizza_id
