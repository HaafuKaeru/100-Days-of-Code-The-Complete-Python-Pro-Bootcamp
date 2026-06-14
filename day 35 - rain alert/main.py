import requests
import pandas as pd
from pprint import pprint


WEATHER_API = "https://api.openweathermap.org/data/2.5/forecast"
API_KEY = "58dc4bada94ab334bdd9aa2c5f0b880f"
# MY_LAT = 52.205338  # cambridge
# MY_LON = 0.121817
MY_LAT = 45.815010  # zagreb
MY_LON = 15.981919

def main():
    params = {
        "lat": MY_LAT,
        "lon": MY_LON,
        "appid": API_KEY,
        "units": "metric",
        "cnt": 4,
    }

    rsp = requests.get(WEATHER_API, params=params)
    rsp.raise_for_status()
    weather_data = dict(rsp.json())
    # print(weather_data)
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
    pprint(user_data)

    # check if it will rain
    will_rain = False
    for hour in user_data:
        if hour["id"] < 700:
            will_rain = True
    if will_rain:
        print("Bring an umbrella!")


if __name__ == '__main__':
    main()