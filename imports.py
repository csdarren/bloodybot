import discord as cord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv(".env")

def get_cord_token():
	return os.getenv("CORD_TOKEN")

def get_weather_key():
	return os.getenv("WEATHER_KEY")

def get_user_location():
	return {
		"CITY": os.getenv("CITY"),
		"STATE": os.getenv("STATE"),
		"COUNTRY": os.getenv("COUNTRY"),
		"ZIP": os.getenv("ZIP"),
	}