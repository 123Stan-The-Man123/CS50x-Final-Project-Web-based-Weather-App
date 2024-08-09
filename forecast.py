import requests
import json

# Uses open-meteo's forecast API: https://open-meteo.com/en/docs

def get_forecast(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast?"

    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "precipitation_probability", "precipitation", "weather_code"],
        "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "sunrise", "sunset", "daylight_duration", "wind_speed_10m_max", "wind_direction_10m_dominant"]
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data:
            return data
        else:
            return "No results found."
    
    except requests.exceptions.RequestException() as e:
        return f"error: {e}"