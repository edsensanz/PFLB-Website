#This is the file where the flask app is created
#The database is also created and linked to the falsk app in the file aswell, the user is loaded (if there is one signed in)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()

#create flask app, link database, import info from other files realted to url linking, load user
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    db.init_app(app)

    #register the blueprint files so that the page directories work and can send and recieve information
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    #import info from user database table
    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    #load user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

#create database
def create_database(app):
    if not path.exists('website/' + 'database.db'):
        db.create_all(app=app)
        #confirmation to the terminal window that the database was created successfully
        print('We got database bois!')
