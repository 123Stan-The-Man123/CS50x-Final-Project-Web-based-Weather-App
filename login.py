from functools import wraps
from flask import session, request, redirect, url_for

# https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/

def login_required(f):
    
    # Retains attributes even when wrapped by another function
    @wraps(f)

    # Accept positional and keyword arguments
    def decorated_function(*args, **kwargs):

        # If there is no user_id (not logged in), the user is redirected to the login page
        if session.get("user_id") is None:
            return redirect("/login")
        
        # If the user is logged in, return to normal function
        return f(*args, **kwargs)

    return decorated_function