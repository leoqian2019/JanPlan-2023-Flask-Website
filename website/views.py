
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


@views.route('/remove/<string:note_id>', methods=['GET'])
def remove(note_id):
    note = db.session.query(Note).filter_by(id=note_id).first()
    db.session.delete(note)
    db.session.commit()

    return redirect(url_for('views.home'))

@views.route('/dashboard/', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)