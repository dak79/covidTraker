from functools import wraps
from flask import session, flash, redirect
import requests
import requests_cache


# Protect pages where log in is required
def login_required(f):
    ''' Decorate route where log in is required '''

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') is None:
            flash('Invalid access, log in', 'danger')
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function


# Custom filter
def mil(value):
    '''Format milion human readable.'''
    return f'{value:,}'


# Cache API answer for 10 minuts
requests_cache.install_cache(
    'covid_cache', backend='sqlite', expire_after=600)


# Requests data to API
def api_general_request(vaccines_or_cases, location):
    ''' Data from API, arguments: 'vaccines' or 'cases', '?country=' + Contry name'''
    base_url = 'https://covid-api.mmediagroup.fr/v1/'
    url = ''.join([base_url, str(vaccines_or_cases), str(location)])
    search = requests.get(url).json()
    return search


def country_cases(cases):
    '''Grab and prepare data for cases database'''
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

    return country, population, confirmed, confirmed_percent, recovered, recovered_percent, deaths, deaths_percent,
    updated


def country_vaccines(vaccination):
    '''Grab and prepare data for vaccines database'''
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

    return country, population, administered_vaccines, totally_vaccinated, totally_vaccinated_percent,
    partially_vaccinated, partially_vaccinated_percent, updated
