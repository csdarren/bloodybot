import requests
from imports import *
import json

weather_key = get_weather_key()
user_location = get_user_location()
# Build weather api call

def get_location(api_key, city="", state_code="", country_code="", limit=""):
	url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state_code},{country_code}&limit={limit}&appid={api_key}"	
	return requests.get(url=url).json()

def get_weather(lat, lon, key):
	url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={key}&units=imperial"
	return requests.get(url=url).json()

def build_weather_report():
	location = get_location(weather_key, user_location["CITY"], user_location["STATE"], user_location["COUNTRY"])
	top_result = location[0]

	weather_data = get_weather(top_result["lat"], top_result["lon"], weather_key)

	location = weather_data["name"]
	temp = weather_data["main"]["temp"]
	wind_speed = weather_data["wind"]["speed"]
#	wind_gust = weather_data["wind"]["gust"]
	return (
		f"location: {location}\n"
		f"temp: {temp}\n"
		f"wind speed: {wind_speed}\n"
		#f"wind gust: {wind_gust}\n"
	)

weather = build_weather_report()

print(f"Weather: {weather}")
