from flask import render_template, request, redirect, session, url_for
from flask_app import app
from flask_app.models import user
from flask_app.models import pizza
from flask_app.models.order import Order

@app.route("/orders/form")
def order_form():
    user_id = session['user_id']
    return render_template("craft_a_pizza.html")

@app.route("/orders/<int:id>")
def order(id):
    data = {
        "id" : id
    }
    order = Order.get_by_id(data)
    return render_template("order.html", order = order)

@app.route('/orders/view')
def view_order():
    if 'user_id' not in session:
        return redirect('/')
    user_id = session['user_id']
    orders = Order.get_orders_by_user_id(user_id)
    return render_template('order.html', orders=orders)


@app.route("/orders/save", methods=["post"])
def save_order():
    data = {
        "name" : request.form["name"],
        "method" : request.form["method"],
        "size" : request.form["size"],
        "toppings" : request.form["toppings"],
        "crust" : request.form["crust"],
        "qty" : request.form["qty"],
        "user_id" : request.form["user_id"]
    }
    Order.save(data)
    return redirect("/dashboard")


@app.route("/orders/<int:id>/update", methods=["post"])
def update_order(id):
    data = {
        "id" : id,
        "name" : request.form["name"],
        "method" : request.form["method"],
        "size" : request.form["size"],
        "toppings" : request.form["toppings"],
        "qty" : request.form["qty"],
        "user_id" : request.form["user_id"]
    }
    Order.update(data)
    return redirect("/dashboard")


@app.route("/orders/<int:id>/delete")
def delete_order(id):
    data = {
        "id" : id
    }
    Order.delete(data)
    return redirect("/dashboard")

