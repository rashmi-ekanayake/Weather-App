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
        current_time = local_time.strftime("%I:%M %p")  # Fix 24h -> 12h format
        current_date = local_time.strftime("%A, %B %d")
        
        time_label.config(text=f"{current_date} | {current_time}")
        city_label.config(text=f"Weather in {city.capitalize()}")

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
        
        wind_card_value.config(text=f"{json_data['wind']['speed']} m/s")  # corrected 'mps' to 'm/s'
        humidity_card_value.config(text=f"{json_data['main']['humidity']}%")
        conditions_card_value.config(text=description)
        pressure_card_value.config(text=f"{json_data['main']['pressure']} hPa")
        
        if "sattered" in description.lower():
            conditions_card_value.config(text=description.replace("Sattered", "Scattered"))

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{str(e)}")


# Search bar
search_frame = Frame(root, bg=ACCENT_COLOR, height=60)
search_frame.pack(fill=X, padx=20, pady=20)

textfield = Entry(search_frame, font=("Arial", 16), bd=0, bg="#ffffff", fg=TEXT_COLOR)
textfield.pack(side=LEFT, padx=15, pady=10, ipady=5, fill=X, expand=True)
textfield.focus()
textfield.bind("<Return>", lambda e: getWeather())

search_btn = Button(search_frame, text="Search", font=("Arial", 12, "bold"), 
                   bg="#ffffff", fg=ACCENT_COLOR, bd=0, command=getWeather)
search_btn.pack(side=RIGHT, padx=15)

# Main weather display
main_frame = Frame(root, bg=BG_COLOR)
main_frame.pack(pady=10, fill=BOTH)

# City and time
city_label = Label(main_frame, font=("Arial", 16, "bold"), bg=CARD_COLOR, fg=TEXT_COLOR)  # bg changed to CARD_COLOR (#ffffff)
city_label.pack(pady=(5, 15))

time_label = Label(main_frame, font=("Arial", 14), bg=BG_COLOR, fg=SECONDARY_COLOR)
time_label.pack()

# Temperature display
temp_frame = Frame(main_frame, bg=BG_COLOR)
temp_frame.pack(pady=10)

temp_label = Label(temp_frame, font=("Arial", 48, "bold"), bg=BG_COLOR, fg="#000000")
temp_label.pack(side=RIGHT)

condition_label = Label(temp_frame, font=("Arial", 14), bg=BG_COLOR, fg=SECONDARY_COLOR)
condition_label.pack(side=LEFT, padx=5, pady=10)

# Weather cards
cards_frame = Frame(root, bg=BG_COLOR)
cards_frame.pack(pady=20, padx=20, fill=BOTH, expand=True)

def create_card(parent, title):
    card = Frame(parent, bg=CARD_COLOR, padx=15, pady=15, bd=1,  
                highlightthickness=0, relief="ridge")
    card.pack(side=LEFT, padx=10, fill=BOTH, expand=False) 
    
    Label(card, text=title, font=("Arial", 12, "bold"), bg=CARD_COLOR, fg=SECONDARY_COLOR).pack(anchor="w")
    
    value = Label(card, text="...", font=("Arial", 18), bg=CARD_COLOR, fg=TEXT_COLOR)  
    value.pack(pady=5)
    
    Label(card, text=title.lower(), font=("Arial", 10), bg=CARD_COLOR, fg=SECONDARY_COLOR).pack(anchor="w")  
    
    return value

# Create cards
wind_card_value = create_card(cards_frame, "WIND")
humidity_card_value = create_card(cards_frame, "HUMIDITY")
conditions_card_value = create_card(cards_frame, "CONDITIONS")
pressure_card_value = create_card(cards_frame, "PRESSURE")
