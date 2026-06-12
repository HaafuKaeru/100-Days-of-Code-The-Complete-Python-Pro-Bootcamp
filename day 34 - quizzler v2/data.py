import requests


API_URL = "https://opentdb.com/api.php"

category = {
    "general": 9,
    "science/nature": 17,
    "cs": 18,
    "geography": 22,
    "history": 23,
    "politics": 24,
    "anime": 31,
    "animation": 32,
}

def get_data(topic: str) -> list:
    params = {
        "amount": 10,
        "type": "boolean",
        "category": category[topic],
    }
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    print(response)
    question_data = response.json()["results"]
    return question_data