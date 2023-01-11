
from . import db
from flask_login import UserMixin

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    permission = db.Column(db.Integer) # 0 = super admin, 1 = coach
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    notes = db.relationship('Note')