from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def create():
    return render_template('login.html')

@app.route('/create_an_account')
def new_register():
    return render_template('register.html')

@app.route('/register', methods = ['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/create_an_account')
    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "address" : request.form["address"],
        "city" : request.form["city"],
        "state" : request.form["state"],
        "password" : bcrypt.generate_password_hash(request.form["password"])
    }
    id = User.save(data)
    session['user_id'] = id

    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user: 
        flash("Invalid Email", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password", "login")
        return redirect('/')
    session['user_id'] = user.id
    print("user_id stored in session:", session['user_id'])
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }

    return render_template("dashboard.html", user = User.select_user(data))

@app.route('/my_account/<int:user_id>')
def edit_account(user_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id' : user_id
    }
    return render_template('account_info.html', user = User.select_user(data))

@app.route('/my_account/process/<int:user_id>', methods = ['POST'])
def update_account_info(user_id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not User.validate_account_update(request.form):
        return redirect(f'/my_account/{user_id}')
    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "address" : request.form["address"],
        "city" : request.form["city"],
        "state" : request.form["state"]
    }
    User.update(data)
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/my_account/info')
def account_info():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    return render_template("account_info.html", user=User.select_user(data))
