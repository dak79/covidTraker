from flask import Flask, render_template, request, redirect, flash, session
from forms import RegistrationForm, LoginForm, CountryCases, CountryVaccines
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, mil, vaccine_request, vaccine_request_specific, cases_request, cases_request_specific
from models import db, Users, Cases, Vaccines
from flask_session import Session
import os
from datetime import timedelta


# Initializing app
app = Flask(__name__)

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///covidtracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=20)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Inizialize db
db.init_app(app)

# Inizialize Session
Session(app)

# Custom filter
app.jinja_env.filters["mil"] = mil


# Route to homepage, global data
@app.route('/')
def index():
    ''' Homepage '''

    global_cases = cases_request_specific('Global')
    global_vaccination = vaccine_request_specific('Global')

    return render_template('index.html', global_cases=global_cases, global_vaccination=global_vaccination)


# Route to register
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


# Route to logout
@app.route('/logout')
@login_required
def logout():
    ''' User Log Out '''

    # Forget the access
    session.clear()

    return redirect('/')


# Route to dashboard
@app.route('/dashboard')
@login_required
def dashboard():

    cases = Cases.query.filter_by(user_id=session['user_id']).all()
    vaccines = Vaccines.query.filter_by(user_id=session['user_id']).all()

    return render_template('dashboard.html', cases=cases, vaccines=vaccines)


# Route to add country cases to dashboard
@app.route('/add_country_cases', methods=['GET', 'POST'])
@login_required
def add_country_cases():
    form = CountryCases(request.form)

    if request.method == 'POST':
        selected_country = form.country_list_cases.data
        cases = cases_request_specific(selected_country)

        # Grab data for database
        user_id = session['user_id']
        try:
            country = cases['All']['country']
        except KeyError:
            flash('No data available', 'danger')
            return redirect('/add_country_cases')
        try:
            population = cases['All']['population']
        except KeyError:
            flash('No data available', 'danger')
            return redirect('/add_country_cases')
        try:
            confirmed = cases['All']['confirmed']
        except KeyError:
            flash('No data available', 'danger')
            return redirect('/add_country_cases')
        confirmed_percent = round(((confirmed / population) * 100), 2)
        try:
            recovered = cases['All']['recovered']
        except KeyError:
            flash('No data available', 'danger')
            return redirect('/add_country_cases')
        recovered_percent = round(((recovered / confirmed) * 100), 2)
        try:
            deaths = cases['All']['deaths']
        except KeyError:
            flash('No data available', 'danger')
            return redirect('/add_country_cases')
        deaths_percent = round(((deaths / confirmed) * 100), 2)
        try:
            updated = cases['All']['updated']
        except KeyError:
            updated = ''

        result = Cases.query.filter_by(country=country).first()
        if result != None:
            flash('You already follow this country', 'danger')
            return redirect('/add_country_cases')

        # Insert country data in db
        new_country_cases = Cases(user_id, country, population, confirmed, confirmed_percent,
                                  recovered, recovered_percent, deaths, deaths_percent, updated)
        db.session.add(new_country_cases)
        db.session.commit()

        return redirect('/dashboard')

    return render_template('add_country_cases.html', form=form)


@app.route('/add_country_vaccination', methods=['POST', 'GET'])
@login_required
def add_country_vaccination():
    form = CountryVaccines(request.form)

    if request.method == 'POST':
        selected_country = form.country_list_vaccines.data
        vaccination = vaccine_request_specific(selected_country)

        # Grab data for database
        user_id = session['user_id']
        try:
            country = vaccination['All']['country']
        except KeyError:
            flash('No data available', 'danger')
            return redirect('/add_country_vaccination')
        try:
            population = vaccination['All']['population']
        except KeyError:
            flash('No data available', 'danger')
            return redirect('/add_country_vaccination')
        try:
            administered_vaccines = vaccination['All']['administered']
        except KeyError:
            flash('No data available', 'danger')
            return redirect('/add_country_vaccination')
        try:
            totally_vaccinated = vaccination['All']['people_vaccinated']
        except KeyError:
            flash('No data available', 'danger')
            return redirect('/add_country_vaccination')

        totally_vaccinated_percent = round(
            ((totally_vaccinated / population) * 100), 2)
        try:
            partially_vaccinated = vaccination['All']['people_partially_vaccinated']
        except KeyError:
            flash('No data available', 'danger')
            return redirect('/add_country_vaccination')
        partially_vaccinated_percent = round(
            ((partially_vaccinated / population) * 100), 2)
        try:
            updated = vaccination['All']['updated']
        except KeyError:
            updated = ''

        result = Vaccines.query.filter_by(country=country).first()
        if result != None:
            flash('You already follow this country', 'danger')
            return redirect('/add_country_vaccination')

        # Insert country data in db
        new_country_vaccines = Vaccines(user_id, country, population, administered_vaccines, totally_vaccinated,
                                        totally_vaccinated_percent, partially_vaccinated, partially_vaccinated_percent, updated)
        db.session.add(new_country_vaccines)
        db.session.commit()

        return redirect('/dashboard')

    return render_template('add_country_vaccination.html', form=form)


# Route to delete case from dashboard
@app.route('/delete_case/<id>', methods=['POST'])
@login_required
def delete_case(id):
    Cases.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Data deleted', 'success')
    return redirect('/dashboard')


# Route to delete vaccine from dashboard
@app.route('/delete_vaccine/<id>', methods=['POST'])
@login_required
def delete_vaccine(id):
    Vaccines.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Data deleted', 'success')
    return redirect('/dashboard')


# Route to update case in dashboard
@app.route('/update_case/<id>', methods=['POST'])
@login_required
def update_case(id):
    location = Cases.query.filter_by(id=id).first()

    new_data = cases_request_specific(location.country)

    # Grab new data for database
    try:
        country = new_data['All']['country']
    except KeyError:
        flash('No data available', 'danger')
        return redirect('/dashboard')
    try:
        population = new_data['All']['population']
    except KeyError:
        flash('No data available', 'danger')
        return redirect('/dashboard')
    try:
        confirmed = new_data['All']['confirmed']
    except KeyError:
        flash('No data available', 'danger')
        return redirect('/dashboard')
    confirmed_percent = round(((confirmed / population) * 100), 2)
    try:
        recovered = new_data['All']['recovered']
    except KeyError:
        flash('No data available', 'danger')
        return redirect('/dashboard')
    recovered_percent = round(((recovered / confirmed) * 100), 2)
    try:
        deaths = new_data['All']['deaths']
    except KeyError:
        flash('No data available', 'danger')
        return redirect('/dashboard')
    deaths_percent = round(((deaths / confirmed) * 100), 2)
    try:
        updated = new_data['All']['updated']
    except KeyError:
        updated = ''

    # Update database
    Cases.query.filter_by(id=id).update(dict(country=country, population=population, confirmed=confirmed, confirmed_percent=confirmed_percent,
                                             recovered=recovered, recovered_percent=recovered_percent, deaths=deaths, deaths_percent=deaths_percent, updated=updated))
    db.session.commit()
    return redirect('/dashboard')


# Route to update case in dashboard
@app.route('/update_vaccine/<id>', methods=['POST'])
@login_required
def update_vaccine(id):
    location = Vaccines.query.filter_by(id=id).first()

    new_data = vaccine_request_specific(location.country)

    # Grab new data for database
    try:
        country = new_data['All']['country']
    except KeyError:
        flash('No data available', 'danger')
        return redirect('/dashboard')
    try:
        population = new_data['All']['population']
    except KeyError:
        flash('No data available', 'danger')
        return redirect('/dashboard')
    try:
        administered_vaccines = new_data['All']['administered']
    except KeyError:
        flash('No data available', 'danger')
        return redirect('/dashboard')
    try:
        totally_vaccinated = new_data['All']['people_vaccinated']
    except KeyError:
        flash('No data available', 'danger')
        return redirect('/dashboard')
    totally_vaccinated_percent = round(
        ((totally_vaccinated / population) * 100), 2)
    try:
        partially_vaccinated = new_data['All']['people_partially_vaccinated']
    except KeyError:
        flash('No data available', 'danger')
        return redirect('/dashboard')
    partially_vaccinated_percent = round(
        ((partially_vaccinated / population) * 100), 2)
    try:
        updated = new_data['All']['updated']
    except KeyError:
        updated = ''

    # Update database
    Vaccines.query.filter_by(id=id).update(dict(country=country, population=population, administered_vaccines=administered_vaccines, totally_vaccinated=totally_vaccinated,
                                                totally_vaccinated_percent=totally_vaccinated_percent, partially_vaccinated=partially_vaccinated, partially_vaccinated_percent=partially_vaccinated_percent, updated=updated))
    db.session.commit()
    return redirect('/dashboard')


# Route to data by_country
@app.route('/by_country')
def by_country():

    cases_by_country = cases_request()

    return render_template('by_country.html', cases_by_country=cases_by_country)


# Route to vaccination data
@app.route('/vaccination')
def vaccination():

    vaccination_by_country = vaccine_request()

    return render_template('vaccination.html', vaccination_by_country=vaccination_by_country)


# Lunch app
if __name__ == '__main__':
    app.run(debug=True)
