
import requests
import os
from dotenv import load_dotenv

def get_weather_data(API, lat, lon):
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={API}&units=imperial"
    response = requests.get(url)
    return response.json()

### Fetching API key and local coordinates ###
load_dotenv()
API = os.getenv("OPENWEATHER_API_KEY")
lat = os.getenv("LAT")
lon = os.getenv("LON")

### Fetching weather data ###
weather_data = get_weather_data(API, lat, lon)

print(API)
print(lat)
print(lon)

print()
print(weather_data)


### Extracting relevant weather data ###
Temps = []
Feels = []
Precip = []
Winds = []
for hour in weather_data['hourly'][:24]:
    Temps.append(hour['temp'])
    Feels.append(hour['feels_like'])
    Precip.append(hour.get('pop', 0) * 100)
    Winds.append(hour['wind_speed'])

maxTemp = max(Temps)
maxFeels = max(Feels)
maxWinds = max(Winds)

minTemp = min(Temps)
minFeels = min(Feels)
minWinds = min(Winds)

sumPrecip = sum(Precip)

### Clothing Options ###
Hat = True
CoatList = ['Puffer 🧥', 'Hoodie', 'Light Jacket', False]
TopList = ['T-Shirt 👕', 'Crew Neck', 'Long Sleeve ']
BottomList = ['Pants 👖', 'Shorts 🩳']
ShoeList = ['Boots 🥾', 'Sneakers 👟']
AccessoryList = ['Rain Jacket 🌧️', 'Umbrella ☔']

### Clothing Logic ###
if sumPrecip > 25 and maxWinds < 10:
    Accessory = AccessoryList[1]
    Top = TopList[0]
    Shoes = ShoeList[0]
elif sumPrecip > 10:
    Accessory = AccessoryList[0]
    Shoes = ShoeList[0]

if maxWinds > 10:
    Hat = False

if minFeels < 30:
    Coat = CoatList[0]
    Top = TopList[2]
    Bottoms = BottomList[0]
    Shoes = ShoeList[0]
elif minFeels < 50:
    Coat = CoatList[1]
    Top = TopList[0]
    Bottoms = BottomList[1]
    Shoes = ShoeList[1]
else:
    Coat = CoatList[3]
    Top = TopList[0]
    Bottoms = BottomList[1]
    Shoes = ShoeList[1]

if maxFeels > 70 and minFeels <= 50:
    Coat = CoatList[2]
    Top = TopList[2]
    Bottoms = BottomList[1]
    Shoes = ShoeList[1]

if Hat == True:
    HatOpt = 'Go ahead'
else:
    HatOpt = 'Skip it'

### Outputting the outfit and weather summary ###
def send_recommendation(HatOpt, Coat, Top, Bottoms, Shoes, maxTemp, minTemp, sumPrecip, maxWinds):
    topic = 'Daily_Outfit_Recs'  # Use your unique name here
    message = 'Today\'s Recommended Outfit:\n' + f'Hat: {HatOpt}\n' + f'Coat: {Coat}\n' + f'Top: {Top}\n' + f'Bottoms: {Bottoms}\n' + f'Shoes: {Shoes}\n\n' + 'Weather Summary for the Next 24 Hours:\n' + f'Max Temperature: {maxTemp}°F\n' + f'Min Temperature: {minTemp}°F\n' + f'Precipitation Probability: {sumPrecip}%\n' + f'Max Wind Speed: {maxWinds} mph'
    
    requests.post(f"https://ntfy.sh/{topic}",
                  data=message.encode('utf-8'),
                  headers={
                      "Title": "Weather & Clothing Bot",
                      "Priority": "high",
                      "Tags": "outfit,clothes,weather"
                  })

send_recommendation(HatOpt, Coat, Top, Bottoms, Shoes, maxTemp, minTemp, sumPrecip, maxWinds)
