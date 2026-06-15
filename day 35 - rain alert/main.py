import requests
import os


MY_LAT = 52.205338  # cambridge
MY_LON = 0.121817
MY_CITY = "Cambridge (UK)"
OPENWEATHER_API_URL = "https://api.openweathermap.org/data/2.5/forecast"
TEXTBEE_API_URL = "https://api.textbee.dev/api/v1"

# to add env variables in windows ps, run this in pycharm terminal or elevated ps and restart pycharm
# [System.Environment]::SetEnvironmentVariable("VARIABLE", "VALUE", "User")


# get weather info
count = 4  # next 12 hours
params = {
    "lat": MY_LAT,
    "lon": MY_LON,
    "appid": os.getenv("OPENWEATHER_API_KEY"),
    "units": "metric",
    "cnt": count,
}
weather_rsp = requests.get(OPENWEATHER_API_URL, params=params)
weather_rsp.raise_for_status()
weather_data = dict(weather_rsp.json())
user_data = []
for forecast in weather_data["list"]:
    info = {
        "temp": int(forecast["main"]["temp"]),
        "feels_like": int(forecast["main"]["feels_like"]),
        "id": min([w["id"] for w in forecast["weather"]]),
        "time": forecast["dt_txt"],
        "main": forecast["weather"][0]["main"],
    }
    user_data.append(info)
print(user_data)

# build notification message
msg = f"Rain is expected in {MY_CITY} in the next {count*3} hours.\n"

# check if it will rain
will_rain = False
rain_hours = []
for hour in user_data:
    if hour["id"] < 700:
        will_rain = True
        rain_hours.append(hour["time"].split(" ")[1].split(":")[0])

additional_msg = f"Specifically, at h{rain_hours[0]}.\n"
if len(rain_hours) > 1:
    additional_msg = f"Specifically, between h{rain_hours[0]} and h{rain_hours[-1]}.\n"
msg += additional_msg
msg += "Grab an umbrella!"

if will_rain:
    text_rsp = requests.post(
        url=f'{TEXTBEE_API_URL}/gateway/devices/{os.getenv("TEXTBEE_PHONE_ID")}/send-sms',
        json={'recipients': [os.getenv("PHONE_NUMBER")], 'message': msg},
        headers={'x-api-key': os.getenv("TEXTBEE_API_KEY")}
    )
    text_rsp.raise_for_status()