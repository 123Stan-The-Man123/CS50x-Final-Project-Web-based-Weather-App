from flask import Flask, render_template, request, jsonify
from geolocate import get_location

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form.get("place")
        information = get_location(query)
        
        return render_template("weather.html", information=information)
    return render_template("index.html")