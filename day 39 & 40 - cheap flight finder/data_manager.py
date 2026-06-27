import requests
import requests_cache
import os


SHEETY_API_URL = "https://api.sheety.co/925e10e3babdda0a58045a4347d329a9/cheapFlightsFromLondon/sheet1"


# create requests caches for testing -> can this become a decorator?
requests_cache.install_cache('sheety_cache')

# This class is responsible for talking to the Google Sheet.
class DataManager:

    def __init__(self):
        self.data = None

    def api_get(self, use_cache=True) -> list[dict]:
        if not use_cache:
            requests_cache.clear()
        header = {
            "Authorization": f"Bearer {os.getenv('SHEETY_WORKOUT_API_BEARER_TOKEN')}"
        }
        rsp = requests.get(
            url=SHEETY_API_URL,
            headers=header,
        )
        rsp.raise_for_status()
        print(f"Source: {'CACHE' if getattr(rsp, 'from_cache', False) else 'API'}")
        self.data = rsp.json()["sheet1"]
        return self.data