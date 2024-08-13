from datetime import datetime
import requests
import json

# Uses open-meteo's forecast API: https://open-meteo.com/en/docs

def get_forecast(lat, lon):
    # Url to query the API
    url = "https://api.open-meteo.com/v1/forecast?"

    # Params to pass into the API
    params = {
        "latitude": lat,
        "longitude": lon,
        "timezone": "auto",
        "hourly": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "precipitation_probability", "weather_code", "wind_speed_10m"],
        "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "sunrise", "sunset", "daylight_duration"]
    }

    # Try to get the response
    try:
        response = requests.get(url, params=params)

        # Check for any errors
        response.raise_for_status()

        # Convert the response into json format
        data = response.json()

        # If the response is not empty, return the data
        if data:
            return data

        # If response was empty, return message
        else:
            return "No results found."
    
    # Throw error in case of exception
    except requests.exceptions.RequestException as e:
        return f"error: {e}"