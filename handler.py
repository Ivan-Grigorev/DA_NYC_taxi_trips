import requests

# API key for WeatherAPI.com
api_key = "ce1a47e57b034d8f853120037211612"

# Base URL for the WeatherAPI.com API
base_url = "http://api.weatherapi.com/v1/history.json?"

# Location to get weather data for
location = "New York City"

# Start and end dates for the date range (YYYY-MM-DD format)
start_date = "2016-01-01"
end_date = "2016-01-31"

# Construct the API request URL
url = base_url + "key=" + api_key + "&q=" + location + "&dt=" + start_date + "&end_dt=" + end_date

# Send the API request and get the response
response = requests.get(url)

# Parse the response JSON data
data = response.json()

# Print the average temperature and total precipitation for the date range
# print("Average temperature in " + location + " from " + start_date + " to " + end_date + " was " + str(data["forecast"]["forecastday"][0]["day"]["avgtemp_f"]) + " degrees Fahrenheit.")
# print("Total precipitation in " + location + " from " + start_date + " to " + end_date + " was " + str(data["forecast"]["forecastday"][0]["day"]["totalprecip_in"]) + " inches.")
print(data)
