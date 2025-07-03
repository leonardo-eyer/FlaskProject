from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from blueprints.app import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__, template_folder="templates")

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            flash("Logged in", category="success")
            login_user(user, remember=True)
            return redirect(url_for("core.index"))

        flash("Incorrect password or email", category="error")

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/signup", methods=['GET', 'POST'])
def signup():

    if request.method == "POST":
        email = request.form['email']
        firstname = request.form['firstname']
        password1 = request.form['password1']
        password2 = request.form['password2']
        if len(email) < 4:
            flash("Email must be at least 4 characters", category="error")
        elif User.query.filter_by(email=email).first():
            flash("Email already registered", category="error")
        elif len(firstname) < 2:
            flash("First name must be at least 2 characters", category="error")
        elif len(password1) < 8:
            flash("Password must be at least 8 characters", category="error")
        elif password1 != password2:
            flash("Passwords don't match", category="error")
        else:
            user = User(
                email = email,
                first_name = firstname,
                password = generate_password_hash(password1)
            )
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            flash("Registration successful", category="success")
            return redirect(url_for('core.index'))

    return render_template("signup.html", user=current_user)