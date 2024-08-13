# Web-Based Weather App
## Video Demo: https://www.youtube.com/watch?v=LysDrnDnjR0
## Description: 
For my cs50x final project, I have made a web-based weather app. Through this project, I have learnt to use API calls (by using the nominatim and open-meteo APIs), as well as solidifying my understanding of Flask. The application has a few basic features:

* Register/Login/Logout system
* Search system (takes location name and geolocates into coordinates for the weather API)
* Bookmark system (save the coordinates of your favourite places for faster access and no API calls)
* Random function (generates random coordinates until it finds a valid location). It is a feature made purely for fun.

### Files
There are a few files in this project. A general overview would be:

* app.py - This covers the main logic of all pages in the app.
* geolocate.py - This takes the name of any location and return its coordinates using the nominatim API, along with some other details.
* forecast.py - Takes the coordinates generated by geolocate.py, retrieving weather data for that location form the open-meteo API. 
* process.py - Takes the coordinates generated by geolocate.py and prepares data for display.
* login.py - Implements the logic for the "@login_required" decorator.
* templates - This directory contains the various html pages required by the app.
* static - Contains the CSS and images used to convey the weather data.

But let's go into more detail.

#### app.py

When the app is started, it begins by initializing itself and adjusting relevant settings. The session is configured to store locally, rather then relying on external cookies. After each request, the cache is disabled in order to prevent the user from going back a page, in the case that they had previously signed out. 

The index function handles the main page of the site, which will be present for most of its use. This is where the search bar form is located, allowing the user to query the API for weather data. The random button is also here, allowing the user to receive a random location's weather data. Once a location has been retrieved, the bookmark form also appears, allowing the user to add the location to their bookmarks. Finally, the weather data will we displayed in tables, including both a detailed and summarised report for a 7 day period.

The random function is called when the random button is pressed. It generates a random set of coordinates, formats them into a string query, and hands them to the geolocation API. If the coordinates are invalid (there is no location), this is repeated until a valid location is found.

The bookmarks function handles the bookmark page and the logic for the bookmark form. If the bookmark button is pressed, it will query the database, checking if that bookmark has already been set by the user. If not, it will insert the relevant details into the database. If the remove button is pressed, it will remove the entry for that user. If the page is loaded, it will fetch all bookmarks from the database with that user's id, displaying them in a table on the page.

The register functions allows users to make an account. It will prompt for a username, password, and confirmation, returning an error if the last 2 do not match. It will then hash the password and query the database for the entered username. If it is present, that means it is already taken, and a message is returned to the screen. If not present, it inserts the relevant details into the users table in the database. Finally, it redirects to the login page.

The login function allows users to log into their accounts. After getting the username and password from the login form, it searches the database for that username. If not present returns invalid username. If present, it hashes the password and checks if the has matches the one in the database. If not, it returns invalid password. If correct, it sets the session id to the user's id and redirects to the home page.

Finally, the logout function allows users to log out of their accounts. It simply clears the session and redirects to index, which in turn redirects to login, due to the "@login_required" decorator.

#### geolocate.py

This program accepts a query, which is either a name or the coordinates generated by the random function. It then queries the nominatim API, returning the name and coordinates of the query, or "No results found." if there is nothing at the query. Can also return an error in exception cases.

#### forecast.py

This program accepts the coordinates generated by the nominatim API. It then queries the open-meteo API, returning the relevant weather data for the location if found. If not found, it returns "No results found." Can also return an error in exception cases.

#### process.py

This program accepts the information generated by the nominatim API, as well as the random flag, which indicates whether this request is coming from the random function or not. Here, the while loop is used if the random coordinates where invalid (there was no location at them), re-generating random coordinates until a valid location is found. If there are no results and the random function did not call the program, it will return the "No results found." message to the homepage. It then gets the forecast from forecast.py and formats the weather data it receives, passing it appropriately into weather.html, depending on if the random function made the call or not.

#### login.py

This program is taken from the flask website. It sets out the rules for the "@login_required" wrapper. If there is no user_id in the session, it will redirect to the login page, otherwise it will proceed as normal. This is called every time a page with the "@login_required" wrapper is loaded.