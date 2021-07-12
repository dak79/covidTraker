from flask import Flask, render_template, request, redirect, flash, session
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import os
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import requests


# Initializing app
app = Flask(__name__)

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///covidtracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Inizialize db
db = SQLAlchemy(app)

# Inizialize Session
Session(app)


# Create database
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


def mil(value):
    """Format milion human readable."""
    return f"{value:,}"


# Custom filter
app.jinja_env.filters["mil"] = mil


# Route to homepage
@app.route('/')
def index():

    # Get global cases from API
    global_cases = requests.get(
        'https://covid-api.mmediagroup.fr/v1/cases?country=Global').json()

    # Get vaccination from API
    global_vaccination = requests.get(
        'https://covid-api.mmediagroup.fr/v1/vaccines?country=Global').json()

    return render_template('index.html', global_cases=global_cases, global_vaccination=global_vaccination)


# Route to register
@ app.route('/register', methods=['GET', 'POST'])
def register():
    ''' User registration '''

    # Instance form
    form = RegistrationForm(request.form)

    # Validation
    if request.method == 'POST' and form.validate():

        # Grab user data
        user = form.username.data
        email = form.email.data
        psw = form.password.data

        # Checking username already existing
        result = Users.query.filter_by(username=user).first()
        if result != None:
            flash('Username already exist', 'danger')
            return redirect('/register')

        # Insert new user in db
        new_user = Users(user, email, generate_password_hash(psw))
        db.session.add(new_user)
        db.session.commit()
        flash('You are successfully registered, please log in', 'success')
        return redirect('/login')

    return render_template('register.html', form=form)


# Route to login
@ app.route('/login', methods=['GET', 'POST'])
def login():
    ''' User Log In '''

    # Instance Form
    form = LoginForm(request.form)

    # Validation
    if request.method == 'POST' and form.validate():

        # Forget any user_id
        session.clear()

        # Grab user data
        user = form.username.data
        psw = form.password.data

        access = Users.query.filter_by(username=user).first()

        # Check username
        if access == None:
            flash('Username not found, please register', 'danger')
            return redirect('/register')

        if access.password == None or not check_password_hash(access.password, psw):
            flash('Incorrect password', 'danger')
            return redirect('/login')

        # Remeber which user logged in
        session['user_id'] = access.id
        session['user'] = access.username
        session['logged_in'] = True
        session['only_cached'] = False

        flash('You successfully logged in', 'success')
        return redirect('/dashboard')

    return render_template('login.html', form=form)


# Protect pages where log in is required
def login_required(f):
    ''' Decorate route where log in is required '''

    @ wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') is None:
            flash('Invalid access, log in', 'danger')
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function


# Route to logout
@ app.route('/logout')
@ login_required
def logout():
    ''' User Log Out '''

    # Forget the access
    session.clear()

    return redirect('/')


# Route to dashboard
@ app.route('/dashboard')
@ login_required
def dashboard():
    # TODO: only if logged in
    return render_template('dashboard.html')


# Route to add country
@ app.route('/add_country')
def add_country():

    # TODO: show all country
    # TODO: think if it is possible using directly by_country.html
    return render_template('add_country.html')


# Route to data by_country
@ app.route('/by_country')
def by_country():
    return render_template('by_country.html')


# Route to vaccination data
@ app.route('/vaccination')
def vaccination():
    return render_template('vaccination.html')


# Lunch app
if __name__ == '__main__':
    app.run(debug=True)
