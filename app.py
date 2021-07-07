from flask import Flask, render_template, request, redirect

# Initializing app
app = Flask(__name__)


# Route to homepage
@app.route('/')
def index():
    # TODO: display dinamic world data from api, manage buttons, mamage dynamic navbar
    return render_template('index.html')


# Route to register
@app.route('/register')
def register():

    # TODO: Use WTF-Form
    # TODO: Username unique and min 4 char, password should match with confirm e min char=4, mail should be a mail. Search form validator for flask.
    # TODO: display clear message for validation, disply message if registration successful
    # TODO: hash password before saving on database
    # TODO: store form in database
    return render_template('register.html')


# Route to login
@app.route('/login')
def login():
    # TODO: check if data are in database,
    # TODO: dehash password for chacking without storing the value in a var,
    # TODO: redirect to dashbord if login is successful and message the user,
    # TODO: dipslay a message if error occure
    # TODO: open session
    return render_template('login.html')


# Route to logout
@app.route('/logout')
def logout():
    # TODO: logout from session
    return redirect('/')


# Route to dashboard
@app.route('/dashboard')
def dashboard():
    # TODO: only if logged in
    return render_template('dashboard.html')


# Route to add country
@app.route('/add_country')
def add_country():

    # TODO: show all country
    # TODO: think if it is possible using directly by_country.html
    return render_template('add_country.html')


# Route to data by_country
@app.route('/by_country')
def by_country():
    return render_template('by_country.html')


# Route to vaccination data
@app.route('/vaccination')
def vaccination():
    return render_template('vaccination.html')


# Lunch app
if __name__ == '__main__':
    app.run(debug=True)
