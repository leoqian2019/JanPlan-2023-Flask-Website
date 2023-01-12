from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
    db.init_app(app)

    from .models import Note, User
    create_database(app)

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    # if not path.exists('website/' + DB_NAME):
    with app.app_context():
        db.create_all()
    print('Created Database!')


def drop_database(app):
    # if path.exists('website/' + DB_NAME):
    with app.app_context():
        db.session.remove()
        db.drop_all()
    print('Dropped Database!')
