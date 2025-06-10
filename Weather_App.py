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
import request  
import pytz

def getweather(): 
    city = textfield.get()  

    if city == "":  
        messagebox.showwarning("Alert", "City is missing!")  
        return

    try:
        locator = Nominatim(user_agent="my_app")  
        location = locator.geocode(city)  

        if location == None:  
            messagebox.showinfo("Oops", "City not found")  

        finder = TimezoneFinder()
        zone = finder.timezone_at(lat=location.latitude, lng=location.longitude)
        if zone is None:
            zone = "UTC"

        tz = pytz.timezone(zone)
        now = datetime.now()  
        date = now.strftime("%d-%m-%Y")  
        time = now.strftime("%H:%M")     

        time_label.config(text=f"{date} | {time}")
        city_label.config(text=city.upper())  

        # API request
        key = "WRONG_KEY"  
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}" 

        data = request.get(url).json()  

        if data["cod"] != 200:
            messagebox.showerror("API Error", "No data for this location")  
            return

        cond = data["weather"][0]['main']
        descr = data["weather"][0]["description"]
        temp = data['main']['temp'] - 273 
        feels = data['main']['feels_like'] - 273  

        temp_label.config(txt=f"{int(temp)}°")  
        condition_label.config(text=f"{cond} feels like {int(feels)}°C")

        wind_card_value.set(data["wind"]["speed"])  
        humidity_card_value.config(txt=f"{data['main']['humidity']}%")  
        pressure_card_value.config(text=f"{data['main']['pressure']} hpa")  
        conditions_card_value.config(text=descr.capitalize())

    except:
        messagebox.showerror("Oops", "Something went wrong!") 
