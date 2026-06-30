import json
import requests
# API endpoint URL
URL = 'https://api.open-meteo.com/v1/forecast?latitude=51.5085&longitude=-0.1257&hourly=temperature_2m&current=temperature_2m'

try:
    # HTTP GET request, to pull the data
    response = requests.get(URL)

    if response.status_code == 200:
        data = response.json()
        print("Successful connection made to the Weather Service API")
        current_temp = data["current"]["temperature_2m"]
        unit = data["current_units"]["temperature_2m"]
        print(f"Current Temperature: {current_temp}{unit}")
    else:
        print(f"Failed to fetch data/read page. Server responded with: {response.status_code}")
    
except requests.exceptions.RequestException as error:
    # Physical connection error handling
    print(f"A connection error has occured: {error}")
