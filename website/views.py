from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from .models import Note
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == "POST":
        note = request.form.get('item')
        new_note = Note(data=note, user_id=current_user.id)

        db.session.add(new_note)
        db.session.commit()
    return render_template("homepage.html", user=current_user, active_page='home')


@views.route('/dashboard/', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user, active_page="dashboard")


@views.route('/setting/', methods=['GET', 'POST'])
@login_required
def setting():
    return render_template("setting.html", user=current_user, active_page="setting")
