from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models import recepie_model, user_model
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if "email" in session:
        return redirect('/recipes')
    return render_template("index.html")

@app.route('/create_user', methods=['POST'])
def create():
    if not user_model.User.validate_form(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
    user_model.User.create(data)
    session['email'] = request.form['email']
    return redirect('/')

@app.route('/login', methods=['POST'])
def log_in():
    data = {
        'email': request.form['email'],
    }
    user_in_db = user_model.User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Credential", "err_log")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
            flash("Invalid Credential", "err_log")
            return redirect('/')
    if user_in_db:
        session['email'] = user_in_db.email
        session['id'] = user_in_db.id
        return redirect('/recipes')

@app.route('/recipes')
def recipes():
    if not "email" in session:
        return redirect('/')
    data = {
        'email': session['email'],
    }
    user = user_model.User.get_by_email(data)
    recipes = recepie_model.Recipe.get_all(data)
    return render_template("recipesShare.html", user=user, recipes=recipes)

@app.route("/logout")
def delete_session():
    session.clear()
    return redirect("/")