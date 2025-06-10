from tkinter import *
import tkinter as tk

# Initialize the root window
root = Tk()
root.title("Weather App")
root.geometry("900x600+300+100")
root.resizable(False, False)
root.configure(bg="#f5f7fa")

# Correct color scheme
BG_COLOR = "#f5f7fa"
CARD_COLOR = "#ffffff"
ACCENT_COLOR = "#3a7bd5"
TEXT_COLOR = "#333333"
SECONDARY_COLOR = "#666666"

from geopy.geocoders import Nominatim
from tkinter import messagebox
from timezonefinder import TimezoneFinder 
from datetime import datetime
import requests
import pytz

def getWeather():
    city = textfield.get().strip()
    
    if city == "":
        messagebox.showerror("Error", "Please enter a city name!")
        return

    try:
        geolocator = Nominatim(user_agent="weather_app")
        location = geolocator.geocode(city, timeout=5)
        
        if location is None:
            messagebox.showerror("Error", "City not found!")
            return

        obj = TimezoneFinder()
        result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
        if not result:
            result = "UTC"
        
        home = pytz.timezone(result)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%H:%M %p")
        current_date = local_time.strftime("%A, %B %d")
        
        time_label.config(text=f"{current_date} | {current_time}")
        city_label.config(text=f"Weather In {city.capitalize()}")

        api_key = "7bdced1c832e8429224004be7d4e090c"
        api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        
        response = requests.get(api, timeout=10)
        json_data = response.json()
        
        if json_data.get("cod") != 200:
            messagebox.showerror("Error", json_data.get("message", "Failed to get weather data"))
            return

        condition = json_data["weather"][0]["main"]
        description = json_data["weather"][0]["description"].capitalize()
        temp_celsius = int(json_data["main"]["temp"] - 273.15)
        feels_like = int(json_data["main"]["feels_like"] - 273.15)
        
        temp_label.config(text=f"{temp_celsius}°C")
        condition_label.config(text=f"{condition} | Feels like {feels_like}°C")
        
        wind_card_value.config(text=f"{json_data['wind']['speed']} mps")
        humidity_card_value.config(text=f"{json_data['main']['humidity']}%")
        conditions_card_value.config(text=description)
        pressure_card_value.config(text=f"{json_data['main']['pressure']} hPa")
        
        if "scattered" in description.lower():
            conditions_card_value.config(text=description.replace("Scattered", "Sattered"))

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
