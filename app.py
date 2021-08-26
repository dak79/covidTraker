from flask import Flask, render_template, request, redirect, flash, session
from forms import RegistrationForm, LoginForm, CountryCases, CountryVaccines
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, mil, api_general_request, country_cases, country_vaccines
from models import db, Users, Cases, Vaccines
from flask_session import Session
import os
from datetime import timedelta


# Instance app
app = Flask(__name__)

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///covidtracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=20)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Init db
db.init_app(app)

# Init Session
Session(app)

# Jinja Custom filter
app.jinja_env.filters["mil"] = mil


@app.route('/')
def index():
    ''' Homepage '''

    global_cases = api_general_request('cases', '?country=Global')
    global_vaccination = api_general_request('vaccines', '?country=Global')

    return render_template('index.html', global_cases=global_cases, global_vaccination=global_vaccination)


@app.route('/by_country')
def by_country():
    ''' Covid-19 cases by Country '''

    cases_by_country = api_general_request('cases', '')

    return render_template('by_country.html', cases_by_country=cases_by_country)


@app.route('/vaccination')
def vaccination():
    ''' Covid-19 vaccination data by Country '''

    vaccination_by_country = api_general_request('vaccines', '')

    return render_template('vaccination.html', vaccination_by_country=vaccination_by_country)


@app.route('/register', methods=['GET', 'POST'])
def register():
    ''' User registration '''

    # Instance form
    form = RegistrationForm(request.form)

    if request.method == 'POST' and form.validate():

        # Grab user data
        user = form.username.data
        email = form.email.data
        psw = form.password.data

        # Checking username already existing
        result = Users.query.filter_by(username=user).first()
        if result is not None:
            flash('Username already exist', 'danger')
            return redirect('/register')

        # Insert new user in db
        new_user = Users(user, email, generate_password_hash(psw))
        db.session.add(new_user)
        db.session.commit()
        flash('You are successfully registered, please log in', 'success')
        return redirect('/login')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    ''' User Log In '''

    # Instance Form
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():

        # Forget any user_id
        session.clear()

        # Grab user data
        user = form.username.data
        psw = form.password.data

        access = Users.query.filter_by(username=user).first()

        # Check username
        if access is None:
            flash('Username not found, please register', 'danger')
            return redirect('/register')

        if access.password is None or not check_password_hash(access.password, psw):
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


@app.route('/logout')
@login_required
def logout():
    ''' User Log Out '''

    # Forget the access
    session.clear()

    return redirect('/')


@app.route('/dashboard')
@login_required
def dashboard():
    ''' User dashboard '''

    cases = Cases.query.filter_by(user_id=session['user_id']).all()
    vaccines = Vaccines.query.filter_by(user_id=session['user_id']).all()

    return render_template('dashboard.html', cases=cases, vaccines=vaccines)


@app.route('/add_country_cases', methods=['GET', 'POST'])
@login_required
def add_country_cases():
    ''' Add favorite Country to dashboard (cases) '''

    form = CountryCases(request.form)

    if request.method == 'POST':
        user_id = session['user_id']
        selected_country = form.country_list_cases.data
        cases = api_general_request('cases', '?country=' + selected_country)

        # Grab data for database
        data = country_cases(cases)
        check = isinstance(data, tuple)

        if check:

            # Check if the result is already in database
            result = Cases.query.filter_by(
                user_id=user_id, country=data[0]).first()
            if result is not None:
                flash('You already follow this country', 'danger')
                return redirect('/add_country_cases')

            # Insert country data in db
            new_country_cases = Cases(
                user_id, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8])
            db.session.add(new_country_cases)
            db.session.commit()

        return redirect('/dashboard')

    return render_template('add_country_cases.html', form=form)


@app.route('/update_case/<id>', methods=['POST'])
@login_required
def update_case(id):
    ''' Update favorite Country (cases) '''

    location = Cases.query.filter_by(id=id).first()

    cases = api_general_request('cases', '?country=' + location.country)

    # Grab new data for database
    data = country_cases(cases)
    result = isinstance(data, tuple)

    if result:
        # Update database
        Cases.query.filter_by(id=id).update(dict(
                    country=data[0], population=data[1], confirmed=data[2],
                    confirmed_percent=data[3], recovered=data[4], recovered_percent=data[5], deaths=data[6],
                    deaths_percent=data[7], updated=data[8]))
        db.session.commit()
    else:
        flash('Update unavailable, try later', 'danger')

    return redirect('/dashboard')


@app.route('/delete_case/<id>', methods=['POST'])
@login_required
def delete_case(id):
    ''' Delete favorite Country (cases) '''

    Cases.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Data deleted', 'success')
    return redirect('/dashboard')


@app.route('/add_country_vaccination', methods=['POST', 'GET'])
@login_required
def add_country_vaccination():
    ''' Add favorite Country to dashboard (vaccination) '''

    form = CountryVaccines(request.form)

    if request.method == 'POST':
        user_id = session['user_id']
        selected_country = form.country_list_vaccines.data
        vaccination = api_general_request(
            'vaccines', '?country=' + selected_country)

        # Grab data for database
        data = country_vaccines(vaccination)
        check = isinstance(data, tuple)

        if check:

            # Check if country is already in database
            result = Vaccines.query.filter_by(
                user_id=user_id, country=data[0]).first()
            if result is not None:
                flash('You already follow this country', 'danger')
                return redirect('/add_country_vaccination')

            # Insert country data in db
            new_country_vaccines = Vaccines(user_id, data[0], data[1], data[2], data[3],
                                            data[4], data[5], data[6], data[7])

            db.session.add(new_country_vaccines)
            db.session.commit()

        return redirect('/dashboard')

    return render_template('add_country_vaccination.html', form=form)


@app.route('/update_vaccine/<id>', methods=['POST'])
@login_required
def update_vaccine(id):
    ''' Update favorite Country (vaccination) '''

    location = Vaccines.query.filter_by(id=id).first()

    vaccination = api_general_request(
        'vaccines', '?country=' + location.country)

    # Grab new data for database
    data = country_vaccines(vaccination)
    result = isinstance(data, tuple)

    if result:
        # Update database
        Vaccines.query.filter_by(id=id).update(dict(
            country=data[0], population=data[1], administered_vaccines=data[2], totally_vaccinated=data[3],
            totally_vaccinated_percent=data[4], partially_vaccinated=data[5], partially_vaccinated_percent=data[6],
            updated=data[7]))
        db.session.commit()
    else:
        flash('Update unavailable, try later', 'danger')

    return redirect('/dashboard')


@app.route('/delete_vaccine/<id>', methods=['POST'])
@login_required
def delete_vaccine(id):
    ''' Delete favorite Country (vaccination) '''

    Vaccines.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Data deleted', 'success')
    return redirect('/dashboard')


# Lunch app
if __name__ == '__main__':
    app.run(debug=True)
