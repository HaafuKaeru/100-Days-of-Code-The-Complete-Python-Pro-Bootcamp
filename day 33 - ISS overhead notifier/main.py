import requests
import datetime as dt
import smtplib


ISS_POSITION_API = "http://api.open-notify.org/iss-now.json"
SUNRISE_SUNSET_API = "https://api.sunrise-sunset.org/json"
MY_LAT = 52.205338 # cambridge
MY_LNG = 0.121817

MY_EMAIL = "pythont090.test@gmail.com"
TARGET_EMAIL = "flavioryu@gmail.com"
MY_PASSWORD = "xxx"
SMTP_ADDRESS = "smtp.gmail.com"


def is_iss_close() -> bool:
    rsp = requests.get(url=ISS_POSITION_API)
    rsp.raise_for_status()
    data = rsp.json()

    latitude = float(data["iss_position"]["latitude"])
    longitude = float(data["iss_position"]["longitude"])
    # print(latitude, longitude)

    if MY_LNG - 5 <= longitude <= MY_LNG + 5 and MY_LAT - 5 <= latitude <= MY_LAT + 5:
        return True
    return False


def is_dark_now() -> bool:
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0,
    }
    response = requests.get(SUNRISE_SUNSET_API, params=parameters)
    response.raise_for_status()
    data = response.json()["results"]

    sunrise = int(data["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["sunset"].split("T")[1].split(":")[0])
    current_hour = dt.datetime.now().hour

    if sunset + 1 < current_hour or current_hour < sunrise - 1:
        return True
    return False


def main():
    if is_dark_now():
        text = "not near Cambridge :(\n\nCheck again another time!"
        if is_iss_close():
            text = "near Cambridge!\n\nGo outside and find it!"
        with smtplib.SMTP(SMTP_ADDRESS) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=TARGET_EMAIL,
                msg=f"Subject:ISS Position Report\n\n"
                    f"The ISS is currently {text}"
            )


if __name__ == '__main__':
    main()