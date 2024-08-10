import requests
import json

#Uses nominatim's geocoding API: https://nominatim.org/release-docs/develop/api/Overview/

def get_location(query):
    url = "https://nominatim.openstreetmap.org/search?"

    headers = {
        "User-Agent": "MyWeatherAppProject {molsas2020@outlook.com}",
        "Accept-Language": "en"
    }

    params = {
        "q": query,
        "format": "json",
        "limit": 1
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if data:
            place = data[0]["name"]
            latitude = data[0]["lat"]
            longitude = data[0]["lon"]

            return {
                "place": place,
                "latitude": latitude,
                "longitude": longitude
            }

        else:
            return "No results found."
    
    except requests.exceptions.RequestException as e:
        return f"An error occured: {e}"