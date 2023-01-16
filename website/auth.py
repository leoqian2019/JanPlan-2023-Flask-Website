from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from .models import Book, User
from flask_login import login_required, current_user, login_user, logout_user
import re

auth = Blueprint('auth', __name__)


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.dashboard'))
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember_me = request.form.get("rememberMe") == 'on'

        user = User.query.filter_by(email=email).first()
        if user:
            if password == user.password:
                login_user(user, remember=remember_me)
                return redirect(url_for('views.dashboard'))
            else:
                return "password is incorrect"
        else:
            return "User does not exist"

    return render_template("login.html", user=current_user, active_page='login')


@auth.route('/logout/', methods=['GET'])
@login_required
def logout():
    current_user.permission = 1
    db.session.commit()

    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup/', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('views.dashboard'))
    elif request.method == 'POST':
        user_name = request.form.get("userName")
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user_name_format_match = re.match(r'^[A-Za-z0-9]{3,}$', user_name)
        email_format_match = re.match(r'^.+@colby.edu$', email)
        password_format_match = re.match(r'.{6,}', password1)

        # user password code from Moodle, this one is quick
        if password1 == password2 and user_name_format_match and email_format_match and password_format_match:
            user = User.query.filter_by(email=email).first()
            if user:
                return "User already exists"
            else:
                if email == "gru@minions.org":
                    permission = 0
                else:
                    permission = 1

                new_user = User(email=email, password=password1, permission=permission, user_name=user_name)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('views.dashboard'))
        elif not user_name_format_match:
            return "Username too short or doesn't match the format, please try again"
        elif not email_format_match:
            return "Not colby email, please try again"
        elif not password_format_match:
            return "Password too short or doesn't match the format, please try again"
        else:
            return "Password doesn't match, please try again"

    return render_template("signup.html", user=current_user, active_page='signup')
