from flask_sqlalchemy import SQLAlchemy

# Init db
db = SQLAlchemy()


# Users table
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


# Cases table
class Cases(db.Model):
    __tablename__ = 'cases'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    country = db.Column(db.Text)
    population = db.Column(db.Integer)
    confirmed = db.Column(db.Integer)
    confirmed_percent = db.Column(db.Float)
    recovered = db.Column(db.Integer)
    recovered_percent = db.Column(db.Float)
    deaths = db.Column(db.Integer)
    deaths_percent = db.Column(db.Float)
    updated = db.Column(db.Text)

    def __init__(self, user_id, country, population, confirmed, confirmed_percent, recovered, recovered_percent, deaths, deaths_percent, updated):
        self.user_id = user_id
        self.country = country
        self.population = population
        self.confirmed = confirmed
        self.confirmed_percent = confirmed_percent
        self.recovered = recovered
        self.recovered_percent = recovered_percent
        self.deaths = deaths
        self.deaths_percent = deaths_percent
        self.updated = updated


# Vaccines table
class Vaccines(db.Model):
    __tablename__ = 'vaccines'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    country = db.Column(db.Text)
    population = db.Column(db.Integer)
    administered_vaccines = db.Column(db.Integer)
    totally_vaccinated = db.Column(db.Integer)
    totally_vaccinated_percent = db.Column(db.Float)
    partially_vaccinated = db.Column(db.Integer)
    partially_vaccinated_percent = db.Column(db.Float)
    updated = db.Column(db.Text)

    def __init__(self, user_id, country, population, administered_vaccines, totally_vaccinated, totally_vaccinated_percent, partially_vaccinated, partially_vaccinated_percent, updated):
        self.user_id = user_id
        self.country = country
        self.population = population
        self.administered_vaccines = administered_vaccines
        self.totally_vaccinated = totally_vaccinated
        self.totally_vaccinated_percent = totally_vaccinated_percent
        self.partially_vaccinated = partially_vaccinated
        self.partially_vaccinated_percent = partially_vaccinated_percent
        self.updated = updated
