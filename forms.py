from wtforms import Form, StringField, PasswordField, SubmitField, SelectField, validators, ValidationError
from wtforms.fields.html5 import EmailField
import email_validator
from helpers import vaccine_request_menu, cases_request_menu


# Registration Form
class RegistrationForm(Form):
    username = StringField(
        'Username', [validators.InputRequired(), validators.Length(min=4, max=30)])
    email = EmailField('Email Address', [
        validators.InputRequired(), validators.Email()])
    password = PasswordField('New Password', [validators.InputRequired(), validators.EqualTo(
        'confirm', message='Passwords must match'), validators.Length(min=6)])
    confirm = PasswordField('Repeat password')
    submit = SubmitField('Confirm Registration')


# Login form
class LoginForm(Form):
    username = StringField(
        'Username', [validators.InputRequired(), validators.Length(min=4, max=30)])
    password = PasswordField(
        'Password', [validators.InputRequired(), validators.Length(min=6)])
    submit = SubmitField('Log In')


# Search country
result_cases = cases_request_menu()


class CountryCases(Form):
    country_list_cases = SelectField(
        'Choose a country', choices=result_cases)
    submit = SubmitField('Add Country')


result_vaccines = vaccine_request_menu()


class CountryVaccines(Form):
    country_list_vaccines = SelectField(
        'Choose a country', choices=result_vaccines)
    submit = SubmitField('Add Country')
