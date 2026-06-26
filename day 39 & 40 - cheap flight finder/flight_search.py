import requests
import requests_cache
from datetime import datetime
import numpy as np


SERPAPI_API_URL = "https://serpapi.com/search?engine=google "
SERPAPI_API_KEY = "xxx"


# This class is responsible for talking to the Flight Search API.
class FlightSearch:

    def __init__(self):
        self.departure = "STN"  # London Stansted
        self.stay_length = 7  # days
        self.outbound_date = None
        self.return_date = None
        self.search_period_limit = None

    def get_dates(self):
        now = datetime.now()
        self.outbound_date = now.date()
        six_months_later = np.add(
            np.datetime64(self.outbound_date),
            np.timedelta64(6, "M"),
            casting="unsafe"
        )
        self.search_period_limit = six_months_later

    def api_get(self, search_params: list[dict]):
        for entry in search_params:
            get_params = {
                "engine": "google_flights",
                "hl": "en",
                "gl": "uk",
                "type": "1",
                "departure_id": self.departure,
                "arrival_id": entry["iata"],
                "outbound_date": self.outbound_date,
                "return_date": self.return_date,
                "currency": "GBP",
            }