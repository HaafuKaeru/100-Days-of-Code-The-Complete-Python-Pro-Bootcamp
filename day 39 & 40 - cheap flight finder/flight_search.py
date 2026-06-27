import requests
import requests_cache
import os
import numpy as np
from datetime import datetime
from dotenv import load_dotenv


SERPAPI_API_URL = "https://serpapi.com/search?engine=google "
load_dotenv("../../.env")

# create requests caches for testing -> can this become a decorator?
requests_cache.install_cache('serpapi_cache')

# This class is responsible for talking to the Flight Search API.
class FlightSearch:

    def __init__(self):
        self.departure = "STN"  # London Stansted
        self.stay_length = 14  # days
        self.outbound_date = None
        self.return_date = None
        self.search_period_limit = None
        self.api_key = os.getenv("SERPAPI_API_KEY")
        self.get_dates()

    def get_dates(self):
        tomorrow = self.calculate_date(1, "D")
        self.outbound_date = tomorrow
        n_days_later  = self.calculate_date(self.stay_length, "D")
        self.return_date = n_days_later
        six_months_later = self.calculate_date(6, "M")
        self.search_period_limit = six_months_later

    def calculate_date(self, amount: int, datetype: str):
        later = np.add(
            np.datetime64(datetime.now().date()),
            np.timedelta64(amount, datetype),
            casting="unsafe"
        )
        return later

    def api_get(self, search_params: list[dict], use_cache=True) -> list:
        if not use_cache:
            requests_cache.clear()
        results = []
        for entry in search_params:
            get_params = {
                "engine": "google_flights",
                "api_key": self.api_key,
                "hl": "en",
                "gl": "uk",
                "type": "1",
                "departure_id": self.departure,
                "arrival_id": entry["iata"],
                "outbound_date": self.outbound_date,
                "return_date": self.return_date,
                "currency": "GBP",
                "sort_by": "2",  # cheapest
                "show_hidden": "true",
            }
            rsp = requests.get(url=SERPAPI_API_URL, params=get_params)
            rsp.raise_for_status()
            print(f"Source: {'CACHE' if getattr(rsp, 'from_cache', False) else 'API'}")
            results.append(rsp.json()["other_flights"][0])  # we already sorted for cheapest so just get the first element
        return results