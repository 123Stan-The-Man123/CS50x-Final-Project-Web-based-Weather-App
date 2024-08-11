from flask import Flask, render_template, redirect, request, jsonify
from geolocate import get_location
from process import process_request
from random import randint

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form.get("place")
        information = get_location(query)

        return process_request(information, False)
        
    return render_template("index.html")

@app.route("/random", methods = ["GET", "POST"])
def random():
    lat = randint(0, 90)
    lon = randint(0, 180)

    query = str(lat) + " " + str(lon)

    information = get_location(query)

    return process_request(information, True)

