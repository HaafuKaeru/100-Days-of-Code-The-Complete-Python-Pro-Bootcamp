import requests
import datetime as dt
import os


WEIGHT = 87
HEIGHT = 165
AGE = 48
GENDER = "female"

# to add env variables in windows ps, run this in pycharm terminal or elevated ps and **restart** pycharm
# [System.Environment]::SetEnvironmentVariable("VARIABLE", "VALUE", "User")

auth_header = {
    "x-app-id": os.getenv("HUNDRED_DAYS_PYTHON_API_APP_ID"),
    "x-app-key": os.getenv("HUNDRED_DAYS_PYTHON_API_KEY"),
    "Content-Type": "application/json",
}

# first, check the server status
server_status_endpoint = f"{os.getenv('HUNDRED_DAYS_PYTHON_API_URL')}/healthz"
rsp = requests.get(server_status_endpoint).json()

if rsp["status"] == "ok":

    # ask user input
    user_input = input("Tell me which exercise you did: ")
    print("\nNutrition API call:")

    natural_lang_endpoint = f"{os.getenv('HUNDRED_DAYS_PYTHON_API_URL')}/v1/nutrition/natural/exercise"
    query_params = {
        # "query": user_input,
        "query": user_input,
        "weight_kg": WEIGHT,
        "height_cm": HEIGHT,
        "age": AGE,
        "gender": GENDER,
    }

    ml_rsp = requests.post(
        url=natural_lang_endpoint,
        headers=auth_header,
        json=query_params,
    )
    ml_rsp.raise_for_status()
    data = ml_rsp.json()["exercises"][0]
    print(data)

    # get exercise data
    now = dt.datetime.now()
    result_dict = {
        "date": now.strftime("%d/%m/%Y"),
        "time": now.strftime("%H:%M:%S"),
        "exercise": data["name"].title(),
        "duration": data["duration_min"],
        "calories": data["nf_calories"],
    }

    # POST request to add row
    print("\nSheety API call:")
    post_req_params = {
        "workout": result_dict
    }
    data_rsp = requests.post(
        url=os.getenv("SHEETY_WORKOUT_API_URL"),
        json=post_req_params,
        headers={"Authorization": f"Bearer {os.getenv('SHEETY_WORKOUT_API_BEARER_TOKEN')}"}
    )
    data_rsp.raise_for_status()
    print(data_rsp.json())
