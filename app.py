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
        if request.form.get("form_id") == "bookmark":
            query = request.form.get("search")
        else:
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

@app.route("/bookmarks", methods=["GET", "POST"])
@login_required
def bookmarks():
    if request.method == "POST":
        if request.form.get("form_id") == "form1":
            id = session["user_id"]
            place = request.form.get("place")
            display = request.form.get("display")
            latitude = float(request.form.get("lat"))
            longitude = float(request.form.get("lon"))

            connection = sqlite3.connect("weather.db")
            cursor = connection.cursor()

            duplicate = cursor.execute("SELECT * FROM bookmarks WHERE user_id = ? AND display = ?", (id, display))
            duplicate = duplicate.fetchone()

            if duplicate != None:
                connection.commit()

                return redirect("/bookmarks")

            cursor.execute("INSERT INTO bookmarks (user_id, place, display, latitude, longitude) VALUES(?, ?, ?, ?, ?)", (id, place, display, latitude, longitude))
            connection.commit()

            return redirect("/bookmarks")
        
        elif request.form.get("form_id") == "remove":
            id = session["user_id"]
            display = request.form.get("remove")

            connection = sqlite3.connect("weather.db")
            cursor = connection.cursor()

            cursor.execute("DELETE FROM bookmarks WHERE user_id = ? AND display = ?", (id, display))

            connection.commit()

            return redirect("/bookmarks")


    else:
        id = session["user_id"]

        connection = sqlite3.connect("weather.db")
        cursor = connection.cursor()

        rows = cursor.execute("SELECT * FROM bookmarks WHERE user_id = ?", (id,))
        rows = rows.fetchall()

        connection.commit()

        return render_template("bookmarks.html", rows=rows)

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

