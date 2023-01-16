from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from .models import Book
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("homepage.html", user=current_user, active_page='home')


@views.route('/dashboard/', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user, active_page="dashboard")


@views.route('/setting/', methods=['GET', 'POST'])
@login_required
def setting():
    return render_template("setting.html", user=current_user, active_page="setting")


@views.route('/textbook/', methods=['GET', 'POST'])
@login_required
def textbook():
    if request.method == 'POST':
        # add new textbook the user has
        if "textbook-user-has" in request.form:
            isbn = request.form.get('isbn')
            book = Book.query.filter_by(isbn=isbn, user_id=current_user.id).first()
            if not book:
                new_isbn = Book(isbn=isbn, user_id=current_user.id, owning_status=1, receiving_status=0)

                db.session.add(new_isbn)
            # if the book already exist, change it to pending pairing state
            else:
                book.owning_status = 1
                book.receiving_status = 0
            db.session.commit()
        # add new textbook the user want
        else:
            isbn = request.form.get('isbn')
            book = Book.query.filter_by(isbn=isbn, user_id=current_user.id).first()
            if not book:
                new_isbn = Book(isbn=isbn, user_id=current_user.id, owning_status=0, receiving_status=0)

                db.session.add(new_isbn)
            # if the book already exist, change it to pending pairing state
            else:
                book.owning_status = 0
                book.receiving_status = 0
            db.session.commit()
    return render_template("textbook.html", user=current_user, active_page="textbook", textbook_page="pair")


def check_if_isbn_is_in_database(isbn):
    pass


@views.route('/textbook_received/', methods=['GET', 'POST'])
@login_required
def textbook_received():
    return render_template("textbook.html", user=current_user, active_page="textbook", textbook_page="received")
