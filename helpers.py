from functools import wraps
from flask import session, flash, redirect


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
