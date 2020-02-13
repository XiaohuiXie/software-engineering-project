# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .user import User
from DarkBoard import Backend, db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    if current_user != None and current_user.is_authenticated:
        if current_user.isTeacher():
            return redirect(url_for("main.teacherHomepage"))
        elif current_user.isStudent():
            return redirect(url_for("main.studentHomepage"))
        else:
            return redirect(url_for("main.adminHomepage"))

    return render_template('index.html')

@auth.route('/login', methods=['POST'])
def login_post():
    if current_user != None and current_user.is_authenticated:
        if current_user.isTeacher():
            return redirect(url_for("main.teacherHomepage"))
        elif current_user.isStudent():
            return redirect(url_for("main.studentHomepage"))
        else:
            return redirect(url_for("main.adminHomepage"))

    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User(username)

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if user.password == "" or not check_password_hash(user.password, password):
        db.db.Logins.update({"ID":user.id}, {"$inc" : {"attempts":1}})
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

    if db.db.Logins.find({"ID":user.id}).next()["attempts"] >= 20:
        flash("Too many login attempts, contact an administrator")
        return redirect(url_for('auth.login'))
    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    if user.isStudent():
        return redirect(url_for('main.studentHomepage'))
    elif user.isAdmin():
        return redirect(url_for('main.adminHomepage'))
    elif user.isTeacher():
        return redirect(url_for('main.teacherHomepage'))


@auth.route('/createAccount', methods=['POST'])
def createAccount():
    # Get form data
    name = request.form.get("name")
    userName = request.form.get("username")
    hashedPassword = generate_password_hash(request.form.get("password"), method='sha256')
    accType = request.form.get("type")
    Backend.createAccount(name, userName, hashedPassword, accType)
    return '', 204

@auth.route('/deleteAccount', methods=['POST'])
def deleteAccount():
    # Get form data
    ID = request.form.get("ID")
    Backend.deleteAccount(ID)
    return '', 204

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


