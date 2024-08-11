from functools import wraps
from flask import session, request, redirect, url_for

# https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/

def login_required(f):
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function