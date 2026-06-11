import requests


API_URL = "https://opentdb.com/api.php"


params = {
    "amount": 10,
    "type": "boolean",
}
response = requests.get(API_URL, params=params)
response.raise_for_status()
question_data = response.json()["results"]