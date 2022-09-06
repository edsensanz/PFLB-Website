#this file create the tables in the database
from . import db
from django.db import models
from flask_login import UserMixin
from sqlalchemy.sql import func


#user table used for logins
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

    objects = models.Manager()

#traps table keeps track of traps and who they belong to
class Traps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trapID = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(150))
    trap_type = db.Column(db.String(150))

#this wil store information on each individual catch
#it will be linked with a many-to-one foreign_key to the traps table to asociate which trap the catch was in
class Catches(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trapID = db.Column(db.Integer)
    email = db.Column(db.String(150))
    species = db.Column(db.String(150))

#simply stores emails for a mailing list
class Newsletter(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)