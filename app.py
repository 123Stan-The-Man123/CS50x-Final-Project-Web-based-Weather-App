from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from flask_login import login_required
from geolocate import get_location
from login import login_required
from process import process_request
from random import uniform
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

# Initialize app
app = Flask(__name__)

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure caching to accomodate the "login_requrired" feature
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# The home page where you search for locations
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":

        # Searches using the bookmark's display name if the POST is coming from the bookmark page
        if request.form.get("form_id") == "bookmark":
            query = request.form.get("search")
        else:
            query = request.form.get("place")
        
        # Converts the place name into coordinates
        information = get_location(query)

        # Hands the details to process.py. False because it is not a random search
        return process_request(information, False)
    
    # Renders the homepage if request was GET
    return render_template("index.html")

@app.route("/random", methods = ["GET", "POST"])
@login_required
def random():

    # Generates random coordinates
    lat = uniform(-90, 90)
    lon = uniform(-180, 180)

    # Formats them into a query
    query = str(lat) + " " + str(lon)

    # Gets the place name at that location or returns error string if there is nothing there (e.g. ocean)
    information = get_location(query)

    # Hands the details to process.py
    return process_request(information, True)

@app.route("/bookmarks", methods=["GET", "POST"])
@login_required
def bookmarks():
    if request.method == "POST":

        # Checks if the "bookmark" button in the homepage was the one pressed
        if request.form.get("form_id") == "form1":

            # Gets all relevant details 
            id = session["user_id"]
            place = request.form.get("place")
            display = request.form.get("display")
            latitude = float(request.form.get("lat"))
            longitude = float(request.form.get("lon"))

            # Establishes connection to "weather.db"
            connection = sqlite3.connect("weather.db")
            cursor = connection.cursor()

            # Checks for duplicates
            duplicate = cursor.execute("SELECT * FROM bookmarks WHERE user_id = ? AND display = ?", (id, display))
            duplicate = duplicate.fetchone()
            
            # Closes connection and redirects to "/bookmarks" if it was a duplicate
            if duplicate != None:
                connection.commit()

                return redirect("/bookmarks")
            
            # Inserts all details into the bookmarks table if not a duplicate and closes connection
            cursor.execute("INSERT INTO bookmarks (user_id, place, display, latitude, longitude) VALUES(?, ?, ?, ?, ?)", (id, place, display, latitude, longitude))
            connection.commit()

            return redirect("/bookmarks")
        
        # Checks if the "remove" button was pressed in the bookmarks page
        elif request.form.get("form_id") == "remove":

            # Get necessary details
            id = session["user_id"]
            display = request.form.get("remove")

            # Establishes connection to "weather.db"
            connection = sqlite3.connect("weather.db")
            cursor = connection.cursor()

            # Deletes the row where the user_id and display match. User id is used here in case multiple users have the same bookmark
            cursor.execute("DELETE FROM bookmarks WHERE user_id = ? AND display = ?", (id, display))

            # Close connection
            connection.commit()

            return redirect("/bookmarks")

    # If request was GET, display all user's bookmarks in a table
    else:

        # Get user id
        id = session["user_id"]
        
        # Establish connection to "weather.db"
        connection = sqlite3.connect("weather.db")
        cursor = connection.cursor()

        # Get all rows from the bookmarks table where the user_id is the current user's id
        rows = cursor.execute("SELECT * FROM bookmarks WHERE user_id = ?", (id,))
        rows = rows.fetchall()

        # Close connection
        connection.commit()

        # Render the bookmarks page, passing in the rows of bookmarks
        return render_template("bookmarks.html", rows=rows)

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":

        # Get the user's details from the form
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Return error if the confirmation is not equal to their proposed password
        if password != request.form.get("confirmation"):
            return render_template("fail.html", error="Password and confirmation do not match.")
        
        # Hashes the password, so it is not readable in the database
        password = generate_password_hash(password, method="pbkdf2", salt_length=16)

        # Establishes connection to "weather.db"
        connection = sqlite3.connect("weather.db")
        cursor = connection.cursor()

        # Search for any users with the same username
        search = cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        search = search.fetchall()

        # Returns error if username is already taken (a row has been found)
        if search != []:
            return render_template("fail.html", error="Username taken.")

        # If not taken, the username and password are inserted into the users table. The id column autoincrements
        cursor.execute("INSERT INTO users (username, password) VALUES(?, ?)", (username, password))

        # Close connection
        connection.commit()

        # Redirect to login page
        return redirect("/login")   
    
    # Renders the register page if method was GET
    return render_template("register.html")

@app.route("/login", methods = ["GET", "POST"])
def login():

    # Forgets the user
    session.clear()

    if request.method == "POST":

        # Get relevant details from the login form
        username = request.form.get("username")
        password = request.form.get("password")

        # Establish connection to "weather.db"
        connection = sqlite3.connect("weather.db")
        cursor = connection.cursor()

        # Get the given users row
        result = cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        details = result.fetchall()

        # If no rows found, return invalid username error
        if len(details) == 0:
            return render_template("fail.html", error="Invalid username")

        # If hashed password does not match the one in the database, invalid password error is returned
        if not check_password_hash(details[0][2], password):
            return render_template("fail.html", error="Invalid password")
        
        # Set the user_id with the value from the users table
        session["user_id"] = details[0][0]

        # Close connection
        connection.commit()
        
        # Go to the homepage
        return redirect("/")
    
    # Renders login page if request was GET
    return render_template("login.html")

@app.route("/logout")
def logout():

    # Clear the user's session, making the app "forget" who they are
    session.clear()

    # Return to the homepage, which in turn will redirect them to the login page
    return redirect("/")

