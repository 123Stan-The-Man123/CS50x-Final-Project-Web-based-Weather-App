from datetime import datetime
from flask import Flask, render_template, request, jsonify
from forecast import get_forecast
from geolocate import get_location
from random import uniform

def process_request(information, flag):
    if information == "No results found." and flag:
        lat = uniform(-90, 90)
        lon = uniform(-180, 180)

        query = str(lat) + " " + str(lon)

        information = get_location(query)
        
        return process_request(information, True)
    
    if information == "No results found.":
        return render_template("index.html", error="No results found.")

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

    display = information["display"].split(",")

    if display[0] == display[-1]:
        name = display[0]
    else:
        name = display[0] + ", " + display[-1]
    
    if flag:
        return render_template("weather.html", place=information["display"], days=days, times=forecast["hourly"]["time"], code=forecast["hourly"]["weather_code"], information=information, forecast=forecast, durations=durations)

    return render_template("weather.html", place=name, days=days, times=forecast["hourly"]["time"], code=forecast["hourly"]["weather_code"], information=information, forecast=forecast, durations=durations)