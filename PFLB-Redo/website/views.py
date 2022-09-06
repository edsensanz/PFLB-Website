#this files does the directories for pages that you simply view and do not send any information to the database
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
from .models import Catches
import json

views = Blueprint('views', __name__)

#home page is set to show up if you have "website_url/" this will mean if they click on any link unless it is specifically to a different page they will be sent here.
@views.route('/')
def home():
    return render_template("home.html", user=current_user)

#This is simply just a page to display all of the images that are used in this website.
@views.route('/gallery')
def gallery():
    return render_template("gallery.html", user=current_user)

#stats page is still currently under development
#will display information from the "traps" and "catches" tables base on the user id
@views.route('/stats')
def stats():
    return render_template("stats.html", user=current_user)