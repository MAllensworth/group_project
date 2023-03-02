from flask_app.config.mysqlconnection import connectToMySQL

class Pizza:
    def __init__(self, method, qty, size, crust, toppings):
        self.method = method
        self.qty = qty
        self.size = size
        self.crust = crust
        self.toppings = toppings

    def __str__(self):
        toppings_str = ', '.join(self.toppings)
        return f"{self.qty} {self.size} {self.crust} pizza with {toppings_str} ({self.method})"

    @classmethod
    def create(cls, method, qty, size, crust, toppings):
        
        query = 'INSERT INTO pizzas(method, qty, size, crust, toppings) VALUES(%s, %s, %s, %s, %s)'
        connectToMySQL('pizza_time').query_db(query, (method, qty, size, crust, ', '.join(toppings)))

        return cls(method, qty, size, crust, toppings)
    
    @classmethod
    def get_by_id(cls, id):
        query = 'SELECT * FROM pizzas WHERE id = %s'
        result = connectToMySQL.query_db(query, (id,), one=True)
        toppings = result['toppings'].split(', ')

        return cls(result['id'], result['method'], result['qty'], result['size'], result['crust'], toppings)
