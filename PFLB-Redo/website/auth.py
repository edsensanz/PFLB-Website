#this file is used to create directories for all of the pages that require a login for them to funtion
#this includes, login page, logout button and the stats page
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from .models import Traps
from .models import Newsletter
from .models import Catches
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user




auth = Blueprint('auth', __name__)

#login page gets the information from the login form and checks it against the database
#first it checks if the email exists in the database
#if the email exists it checks that the password matches
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #get login information from the form
        email = request.form.get('email')
        password = request.form.get('password')

        #check to see if there is a login with the stated email.
        user = User.query.filter_by(email=email).first()
        if user:
            #if there is a user with the email check to see if the sotred password for that email is the same as the supplied one
            if user.password == password:
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                #redirect to the home page once logged in successfully
                return render_template('home.html', user=current_user)
            else:
                #flash if the password does not match the stored one
                flash('Incorrect password, try again.', category='error')
        else:
            #if the email is not found in the database it flashes an error saying that the account doesnt exist.
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

#a simple sign up page that allows users to start trapping and logging information
#this origionally wasnt going to be a publicly accessed page however, just for now I am going to make it accessable to all people so that I can get a working product and go from there.
@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        #get users information from the form
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #check to see if there is an existing user with the same email address
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
            #checking to see if all of the information provided is valid
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            #if all of the supplied information is valid it creates a new table entry
            new_user = User(email=email, first_name=first_name, password=password1)
            db.session.add(new_user)
            db.session.commit()
            #flash to show that the action was successful
            flash('Account created!', category='success')
            #redirect so that the user is automatically logged in if it was successful
            return redirect(url_for('auth.sign_up'))
    
    return render_template("sign_up.html", user=current_user)


#@auth.route('/admin', methods=['GET', 'POST'])
#def admin():
#    if request.method == 'POST':
#        email = request.form.get('email')
#        first_name = request.form.get('firstName')
#        password1 = request.form.get('password1')
#        password2 = request.form.get('password2')
#        is_staff = request.form.get('is_staff')
#
#        user = User.query.filter_by(email=email).first()
#        if user:
#            flash('Email already exists.', category='error')
#        elif len(email) < 4:
#            flash('Email must be greater than 3 characters.', category='error')
#        elif len(first_name) < 2:
#            flash('First name must be greater than 1 character.', category='error')
#        elif password1 != password2:
#            flash('Passwords don\'t match.', category='error')
#        elif len(password1) < 7:
#            flash('Password must be at least 7 characters.', category='error')
#        else:
#            new_user = User(email=email, first_name=first_name, password=password1, is_staff=is_staff)
#            db.session.add(new_user)
#            db.session.commit()
#            flash('Account created!', category='success')
#            return redirect(url_for('auth.admin'))

#    return render_template("admin.html", user=current_user)

#logout button, removes the saved user
@auth.route('/logout')
@login_required
def logout():
    #simply if the button is pressed run the flask function to log out the user
    logout_user()
    #flash to show they are logged out
    flash('Logged out successfully!', category='success')
    #set the user to blank meaning that the page is now in "anonymous" mode. no funcionality requiring user info will work
    return render_template('home.html', user = '')

#This is the profile page, this is how users can add new traps as well as log any catches they get in theirs
@auth.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        #get hidden value from each form to determine which one is being used
        form_type = request.form.get('form_type')

        #new trap form
        if form_type == 'trap':
            #gather all data from the form in variables
            id = request.form.get('trapID')
            #grabs the currently logged in users email address to identify who made the input
            user=current_user
            email = user.email
            trap_type = request.form.get('trap_type')

            #check to see if the trap id that has been gather already exists
            #if it already exists it will flash an error
            trap = Traps.query.filter_by(trapID=id).first()
            if trap:
                flash('Trap already exists.', category='error')
            #simple checks to see if all of the values are as they are expected
            elif len(id) != 4:
                flash("Invalid trap ID. ID's are 4 digit numbers.", category='error')
            elif len(trap_type) < 3:
                flash('Please state the type of trap.', category='error')
            else:
                #check to see if the id submitted is actually an integer
                if id.isdigit():
                    #if all the checks are passed it will create an entry into the database will all of the relevant information
                    new_trap = Traps(trapID=id, email=email, trap_type=trap_type)
                    db.session.add(new_trap)
                    db.session.commit()
                    #flash confirmation schowing that it all worked
                    flash('New trap added!', category='success')
                else:
                    flash("Invalid trap ID. ID's are 4 digit numbers.", category='error')



        #new catch form
        if form_type == 'catch':
            #gather all data from the form
            id = request.form.get('trapID')
            #get current user's email to identify who made the input
            user=current_user
            email = user.email
            species = request.form.get('species')

            #check to see if a trap with the stated id already exists
            #if it doesnt it will flash an error because cataches can only be recorded for existing traps
            trap = Traps.query.filter_by(trapID=id).first()
            if trap:
                #because it doesnt matter if there is a catch that is the same there is no need to check if it is unique
                #other simple checks check to see if the other data is valid
                if len(id) != 4:
                    flash("Invalid trap ID. ID's are 4 digit numbers.", category='error')
                elif len(species) < 3:
                    flash('Please state the species caught', category='error')
                else:
                    #once all the checks are passed the information is sent to the database
                    new_catch = Catches(trapID=id, email=email, species=species)
                    db.session.add(new_catch)
                    db.session.commit()
                    #flash to show that it input correctly
                    flash('New catch recorded!', category='success')
            else:
                flash('Trap does not exist, or trap ID is invalid.', category='error')

    return render_template("profile.html", user=current_user)

#about us page, mostly just information however there is a form on there that will get peoples email adresses and put them into the Newsletter database table for storing in a mailing list
@auth.route('/aboutUs', methods=['GET', 'POST'])
def aboutUs():
    if request.method == 'POST':
        #grab the email that was inputted
        email = request.form.get('email')

        #check to see if the email is already in the database
        mail = Newsletter.query.filter_by(email=email).first()
        if mail:
            #if the email already exists in the datbase flash an error
            flash('Email already signed up.', category='error')
        else:
            #if the email doesnt already exist and it is a valid email (checked by the form requiring a valid email) it will be put into the database
            new_mail = Newsletter(email=email)
            db.session.add(new_mail)
            db.session.commit()
            #flash to show that it was successfully inserted into the database
            flash('Signed Up for Newsletter!', category='success')
    
    return render_template("aboutUs.html", user=current_user)