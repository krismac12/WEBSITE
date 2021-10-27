from flask import ( 
    Blueprint, flash, render_template, request, url_for, redirect
) 
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User
from .forms import Login, Register
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .forms import Register, Login



bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = Login()
    error=None
    if(login_form.validate_on_submit()==True):
        #get the username and password from the database
        user_name = login_form.username.data
        password = login_form.password.data
        u1 = User.query.filter_by(name=user_name).first()
        #if there is no user with that name
        if u1 is None:
            error='Incorrect user name'
        #check the password - notice password hash function
        elif not check_password_hash(u1.password, password): # takes the hash and password
            error='Incorrect password'
        if error is None:
            #all good, set the login_user of flask_login to manage the user
            login_user(u1)
            return redirect(url_for('main.index'))
        else:
            flash(error)
    return render_template('login.html', form=login_form)


@bp.route('/register', methods = ['GET','POST'])
def register():
    register = Register()
    #the validation of form submis is fine
    if (register.validate_on_submit() == True):
            #get username, password and email from the form
            uname =register.username.data
            pwd = register.password.data
            email=register.email_id.data
            #check if a user exists
            u1 = User.query.filter_by(name=uname).first()
            if u1:
                flash('User name already exists, please login')
                return redirect(url_for('auth.login'))
            # don't store the password - create password hash
            pwd_hash = generate_password_hash(pwd)
            #create a new user model object
            new_user = User(name=uname, password=pwd_hash, email=email)
            db.session.add(new_user)
            db.session.commit()
            #commit to the database and redirect to HTML page
            return redirect(url_for('auth.login'))
    #the else is called when there is a get message
    else:
        return render_template('register.html', 
        registerForm = register)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
### THIS IS FROM IAB207 SPEC ###

# this is the hint for a login function
# @bp.route('/login', methods=['GET', 'POST'])
# def authenticate(): #view function
#     print('In Login View function')
#     login_form = LoginForm()
#     error=None
#     if(login_form.validate_on_submit()==True):
#         user_name = login_form.user_name.data
#         password = login_form.password.data
#         u1 = User.query.filter_by(name=user_name).first()
#         if u1 is None:
#             error='Incorrect user name'
#         elif not check_password_hash(u1.password_hash, password): # takes the hash and password
#             error='Incorrect password'
#         if error is None:
#             login_user(u1)
#             nextp = request.args.get('next') #this gives the url from where the login page was accessed
#             print(nextp)
#             if next is None or not nextp.startswith('/'):
#                 return redirect(url_for('index'))
#             return redirect(nextp)
#         else:
#             flash(error)
#     return render_template('user.html', form=login_form, heading='Login')
