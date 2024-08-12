from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from flask_login import login_required
from geolocate import get_location
from login import login_required
from process import process_request
from random import uniform
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        query = request.form.get("place")
        information = get_location(query)

        return process_request(information, False)
        
    return render_template("index.html")

@app.route("/random", methods = ["GET", "POST"])
@login_required
def random():
    lat = uniform(-90, 90)
    lon = uniform(-180, 180)

    query = str(lat) + " " + str(lon)

    information = get_location(query)

    return process_request(information, True)

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if password != request.form.get("confirmation"):
            return render_template("fail.html", error="Password and confirmation do not match.")
        
        password = generate_password_hash(password, method="pbkdf2", salt_length=16)

        connection = sqlite3.connect("weather.db")
        cursor = connection.cursor()

        search = cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        search = search.fetchall()

        if search != []:
            return render_template("fail.html", error="Username taken.")

        cursor.execute("INSERT INTO users (username, password) VALUES(?, ?)", (username, password))

        connection.commit()

        return redirect("/login")   
    
    return render_template("register.html")

@app.route("/login", methods = ["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        connection = sqlite3.connect("weather.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM users WHERE username = ?", (username,))

        details = result.fetchall()

        if len(details) == 0:
            return render_template("fail.html", error="Invalid username")

        if not check_password_hash(details[0][2], password):
            return render_template("fail.html", error="Invalid password")
        
        session["user_id"] = details[0][0]

        connection.commit()
        
        return redirect("/")
    
    return render_template("login.html")

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

