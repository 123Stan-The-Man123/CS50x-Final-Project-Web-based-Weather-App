from datetime import datetime 
from flask import Flask, render_template, request, jsonify
from forecast import get_forecast
from geolocate import get_location

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form.get("place")
        information = get_location(query)

        if information == "No results found.":
            return render_template("weather.html", information=information)
        
        forecast = get_forecast(information["latitude"], information["longitude"])

        days = []
        day = ""

        for i in forecast["daily"]["time"]:
            day = datetime.fromisoformat(i)
            days.append(day.strftime("%A"))
        
        durations = []
        duration = 0

        for i in forecast["daily"]["daylight_duration"]:
            duration = float(i) / 60.0 / 60.0
            duration = round(duration, 2)
            durations.append(duration)
        
        return render_template("weather.html", place=information["place"], days=days, times=forecast["hourly"]["time"], code=forecast["hourly"]["weather_code"], information=information, forecast=forecast, durations=durations)
        
    return render_template("index.html")