from . import db
from flask_login import UserMixin


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(10000))
    # if the user have the textbook, it is 1, else, it is 0
    owning_status = db.Column(db.Integer)
    # 1 == received, 0 == not received
    receiving_status = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    permission = db.Column(db.Integer)  # 0 = super admin, 1 = coach
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    user_name = db.Column(db.String(100))
    books = db.relationship('Book')
