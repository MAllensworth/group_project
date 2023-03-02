from flask_app.controllers import users
from flask_app.controllers import pizzas
from flask_app.controllers import orders

from flask_app import app

if __name__ == '__main__':
    app.run(debug=True, port="5001")