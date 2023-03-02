from flask import Flask, render_template, request, redirect
from flask_app import app
from models.pizza import Pizza


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_pizza', methods=['GET', 'POST'])
def create_pizza():
    if request.method == 'POST':


        method = request.form['method']
        qty = request.form['qty']
        size = request.form['size']
        crust = request.form['crust']
        toppings = request.form.getlist('toppings')

        pizza = Pizza.create(method, qty, size, crust, toppings)

        return redirect(f'/order_pizza/{pizza.id}')

    else:
        return render_template('create_pizza.html')

@app.route('/order_pizza/<int:pizza_id>')
def order_pizza(pizza_id):

    pizza = Pizza.get_by_id(pizza_id)

    if pizza is not None:
        return render_template('order_pizza.html', pizza=pizza)
    else:
        return 'Pizza not found'
    


