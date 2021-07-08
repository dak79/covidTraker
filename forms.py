from wtforms import Form, StringField, PasswordField, SubmitField, validators, ValidationError
from wtforms.fields.html5 import EmailField
import email_validator


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
