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
    """Format milion human readable."""
    return f"{value:,}"


# Cache API answer for 10 minuts
requests_cache.install_cache(
    'covid_cache', backend='sqlite', expire_after=600)


# Requests data to API
def vaccine_request():
    search = requests.get(
        'https://covid-api.mmediagroup.fr/v1/vaccines').json()
    return search


def vaccine_request_menu():
    menu = []
    search = requests.get(
        'https://covid-api.mmediagroup.fr/v1/vaccines').json()
    for country, data in search.items():
        menu.append(country)
    return menu


def vaccine_request_specific(location):
    base_url = 'https://covid-api.mmediagroup.fr/v1/vaccines?country='
    url = ''.join([base_url, str(location)])
    search_vaccine_location = requests.get(url).json()
    return search_vaccine_location


def cases_request():
    search = requests.get(
        'https://covid-api.mmediagroup.fr/v1/cases').json()
    return search


def cases_request_menu():
    menu = []
    search = requests.get(
        'https://covid-api.mmediagroup.fr/v1/cases').json()
    for country, data in search.items():
        menu.append(country)
    return menu


def cases_request_specific(location):
    base_url = 'https://covid-api.mmediagroup.fr/v1/cases?country='
    url = ''.join([base_url, str(location)])
    search_vaccine_location = requests.get(url).json()
    return search_vaccine_location

 # Get global cases from API
   # global_cases = requests.get(
    #    'https://covid-api.mmediagroup.fr/v1/cases?country=Global').json()

    # Get vaccination from API
    # global_vaccination = requests.get(
    #   'https://covid-api.mmediagroup.fr/v1/vaccines?country=Global').json()


# Cases for selected country
    #base_url_cases = 'https://covid-api.mmediagroup.fr/v1/cases?country='
    #url_cases = ''.join([base_url_cases, selected_country])
    #cases = requests.get(url_cases).json()

 # Vaccination for selected country
    #base_url_vaccination = 'https://covid-api.mmediagroup.fr/v1/vaccines?country='
    #url_vaccination = ''.join([base_url_vaccination, selected_country])
    #vaccination = requests.get(url_vaccination).json()
