import os
import dotenv
import requests
import re
from bs4 import BeautifulSoup


dotenv.load_dotenv("../.env")
ZILLOW_CLONE_URL = os.getenv("zillow_clone_url")


class ZillowScraper:

    def __init__(self):
        self.zillow_url = ZILLOW_CLONE_URL
        self.soup = None
        self._make_soup()

    def _make_soup(self):
        rsp = requests.get(self.zillow_url)
        rsp.raise_for_status()
        self.soup = BeautifulSoup(rsp.text, features="html.parser")

    def get_listings(self) -> list[tuple]:
        listings = self.soup.select("div.result-list-container ul")[0]
        houses = listings.select("li[class*='StyledListCardWrapper']")
        result = []
        for house in houses:
            address = self._clean_address(house.select_one("address").text)
            price = self._clean_price(house.select_one("span[data-test*='property-card-price']").text)
            link = house.select_one("a.property-card-link").get('href')
            result.append((address, price, link))
        return result

    @staticmethod
    def _clean_address(string: str) -> str:
        clean = string.strip()
        if "|" in string:
            clean = clean.split("|")[-1]
        else:
            clean = "".join(clean.split(",")[1:])
        return clean.strip()

    @staticmethod
    def _clean_price(string: str):
        return re.match(r'\$\d,*\d+', string).group(0)