import requests
import requests_cache
import os
from dotenv import load_dotenv


load_dotenv(dotenv_path="../../../.env")

# create requests caches for testing -> can this become a decorator?
requests_cache.install_cache('sheety_cache')

# This class is responsible for talking to the Google Sheet.
class DataManager:

    def __init__(self):
        self.data = None
        self.bearer_token = os.getenv('SHEETY_CHEAP_FLIGHTS_API_BEARER_TOKEN')
        self.sheet_prices_url = os.getenv('SHEETY_CHEAP_FLIGHTS_PRICES_API_URL')
        self.sheet_users_url = os.getenv('SHEETY_CHEAP_FLIGHTS_USERS_API_URL')
        self.header = {
            "Authorization": f"Bearer {self.bearer_token}"
        }

    def get_required_flights(self, use_cache=True) -> list[dict]:
        if not use_cache:
            requests_cache.clear()
        rsp = requests.get(
            url=self.sheet_prices_url,
            headers=self.header,
        )
        rsp.raise_for_status()
        print(f"Source: {'CACHE' if getattr(rsp, 'from_cache', False) else 'API'}")
        self.data = rsp.json()["prices"]
        return self.data

    def get_customer_emails(self, use_cache=True):
        if not use_cache:
            requests_cache.clear()
        rsp = requests.get(
            url=self.sheet_users_url,
            headers=self.header,
        )
        rsp.raise_for_status()
        print(f"Source: {'CACHE' if getattr(rsp, 'from_cache', False) else 'API'}")
        self.data = rsp.json()["users"]
        return self.data
