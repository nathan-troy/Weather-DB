import json
import os
import time
import requests

# Defining locations to track, includes coordinates
LOCATIONS = [
    {"name": "London", "lat": 51.51, "lon": -0.13},
    {"name": "Berlin", "lat": 52.52, "lon": 13.41},
    {"name": "Riyadh", "lat": 24.69, "lon": 46.72},
    {"name": "New York", "lat": 40.71, "lon": -74.01},
    {"name": "Sydney", "lat": -33.87, "lon": 151.21},
    {"name": "Beijing", "lat": 39.91, "lon": 116.40},
]

# Setting up the database file name, where the data is saved
DB_FILE = "weather_database.json"

print("Setup Complete!")

# Checking if there is an existing database file
if os.path.exists(DB_FILE):
    # If the file exists already, open it and load the data
    with open(DB_FILE, "r") as file_handle:
        # Using json to read the file
        weather_db = json.load(file_handle)
    print(f"Found existing database with {len(weather_db)} records.")
else:
    # If no file exists yet, start with an empty list
    weather_db = []
    print("No existing database found. Creating a new weather tracking list.")

# Defining connection headers to ensure the API responds with pure data
custom_headers = {"Accept": "application/json", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

for loc in LOCATIONS:
    # Building the unique URL for each specific coordinate pair
    URL = f"https://api.open-meteo.com/v1/forecast?latitude={loc['lat']}&longitude={loc['lon']}&hourly=temperature_2m&current=temperature_2m,wind_speed_10m,relative_humidity_2m&timezone=auto"

    try:
        response = requests.get(URL, headers=custom_headers)

        if response.status_code == 200:
            data = response.json()
            # Dictionary for database field design
            weather_snapshot = {
                "location_name": loc["name"],
                "coordinates": {"lat": loc["lat"], "lon": loc["lon"]},
                "collected_at": data["current"]["time"],
                "current_weather": {
                    "temperature": data["current"]["temperature_2m"],
                    "unit": data["current_units"]["temperature_2m"],
                    "wind_speed": data["current"]["wind_speed_10m"],
                    "humidity": data["current"]["relative_humidity_2m"],
                    "humidity_unit": data["current_units"]["relative_humidity_2m"],
                },
                "hourly_forecast": data["hourly"]["temperature_2m"][
                    0:24
                ], # Stores info for the next 24 hours
            }

            # Append this structured record directly into the running database memory list
            weather_db.append(weather_snapshot)
            print(f"Successfully processed and structured data for {loc['name']}")

        else:
            print(f"Skipped {loc['name']}. Server responded with: {response.status_code}")

    except requests.exceptions.RequestException as error:
        print(f"Network failure connecting to {loc['name']}: {error}")

        # Pausing, as to not overwhelm the API
    time.sleep(5)

print("Saving updates to the database file...")
with open(DB_FILE, "w") as file_handle:
    json.dump(weather_db, file_handle, indent=4)

print(f"Success! Data saved to '{DB_FILE}'. Script complete.")