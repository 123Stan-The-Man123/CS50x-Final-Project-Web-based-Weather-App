import requests
import json

#Uses nominatim's geocoding API: https://nominatim.org/release-docs/develop/api/Overview/

def get_location(query):
    # Url to query the API
    url = "https://nominatim.openstreetmap.org/search?"

    # Required headers
    headers = {
        "User-Agent": "MyWeatherAppProject {molsas2020@outlook.com}",
        "Accept-Language": "en"
    }

    # Params to pass into the API
    params = {
        "q": query,
        "format": "json",
        "limit": 1
    }

    # Try to get the response
    try:
        response = requests.get(url, headers=headers, params=params)

        # Check for any errors
        response.raise_for_status()

        # Convert the response into json format
        data = response.json()

        # If the response is not empty, return the data as a dictionary
        if data:
            place = data[0]["name"]
            display = data[0]["display_name"]
            latitude = data[0]["lat"]
            longitude = data[0]["lon"]

            return {
                "place": place,
                "display": display,
                "latitude": latitude,
                "longitude": longitude
            }

        # If response was empty, return message
        else:
            return "No results found."
    
    # Throw error in case of exception
    except requests.exceptions.RequestException as e:
        return f"An error occured: {e}"