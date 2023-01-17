from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from .models import Book
from flask_login import login_required, current_user
import re

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
        isbn = request.form.get('isbn')
        if isbn and re.match(r'^([0-9]{10}|[0-9]{13})$', isbn):
            book = Book.query.filter_by(isbn=isbn, user_id=current_user.id).first()
            # add new textbook the user has
            if "textbook-user-has" in request.form:
                if not book:
                    new_isbn = Book(isbn=isbn, user_id=current_user.id, owning_status=1, receiving_status=0)
                    db.session.add(new_isbn)
                # if the book already exist, change it to pending pairing state
                else:
                    book.owning_status = 1
                    book.receiving_status = 0
            # add new textbook the user want
            else:
                if not book:
                    new_isbn = Book(isbn=isbn, user_id=current_user.id, owning_status=0, receiving_status=0)
                    db.session.add(new_isbn)
                # if the book already exist, change it to pending pairing state
                else:
                    book.owning_status = 0
                    book.receiving_status = 0
            db.session.commit()
        # mark the list of book ids as received
        elif "mark-receive" in request.form:
            received = request.form.getlist('textbook-own')
            for book_id in received:
                book = Book.query.filter_by(id=book_id).first()
                if book:
                    book.receiving_status = 1
            db.session.commit()
        # delete the list of book ids from the Book database
        elif "delete" in request.form:
            to_delete = request.form.getlist('textbook-own')

            for book_id in to_delete:
                book = Book.query.filter_by(id=book_id).first()
                if book:
                    db.session.delete(book)
            db.session.commit()
        else:
            return "The isbn you entered is not correct, please try again"
    return render_template("textbook.html", user=current_user, active_page="textbook", textbook_page="pair")



@views.route('/textbook_received/', methods=['GET', 'POST'])
@login_required
def textbook_received():
    if "delete" in request.form:
        to_delete = request.form.getlist('textbook-own')

        for book_id in to_delete:
            book = Book.query.filter_by(id=book_id).first()
            if book:
                db.session.delete(book)
        db.session.commit()
    return render_template("textbook.html", user=current_user, active_page="textbook", textbook_page="received")


