import json
import os

DB_FILE = "weather_database.json"
# Check if the database exists before attempting to read it
if not os.path.exists(DB_FILE):
    print(f"Error: Database file {DB_FILE} does not exist.")
    exit()

# Load the JSON database into memory
with open(DB_FILE, "r") as file_handle:
    weather_db = json.load(file_handle)

print("=" * 105)
print(f"{'CITY':<15} | {'TIMESTAMP':<18} | {'CURRENT TEMP':<15} | {'WIND SPEED':<12} | {'HUMIDITY':<10} | {'24H MIN / MAX'}")
print("=" * 105)

# Translate the NoSQL data into a tabular view, making it easier to read for others (Data analysts, Meteorologists, etc)
for entry in weather_db:
    name = entry["location_name"]
    time = entry["collected_at"].replace("T", " ") # Clean up the timestamp formatting

    temp = entry["current_weather"]["temperature"]
    temp_unit = entry["current_weather"]["unit"]
    

    wind = entry["current_weather"].get("wind_speed", "N/A")
    wind_unit = entry["current_weather"].get("wind_unit", "km/h")
    
    humidity = entry["current_weather"].get("humidity", "N/A")
    humid_unit = entry["current_weather"].get("humidity_unit", "%")

    # Calculate tabular summary statistics out of hourly array data
    hourly_forecast = entry["hourly_forecast"]
    min_temp = min(hourly_forecast)
    max_temp = max(hourly_forecast)

    # Format variables dynamically into aligned table rows
    current_display = f"{temp}{temp_unit}"
    range_display = f"{min_temp}{temp_unit} to {max_temp}{temp_unit}"
    wind_display = f"{wind} {wind_unit}".strip()
    humidity_display = f"{humidity}{humid_unit}".strip()

    print(f"{name:<15} | {time:<18} | {current_display:<15} | {wind_display:<12} | {humidity_display:<10} | {range_display}")

print("=" * 105)
print(f"Tabular view compiled from {len(weather_db)} raw NoSQL records")


