import os
import dotenv
import requests

from bs4 import BeautifulSoup


dotenv.load_dotenv("../.env")


def requests_headers():
    return {
        "User-Agent": os.getenv("user_agent"),
        "Accept-Language": os.getenv("accept_language")
    }


class AmazonScraper:

    def __init__(self, url: str):
        self.url = url
        self.soup = None
        self._make_soup()

    def _make_soup(self):
        rsp = requests.get(url=self.url, headers=requests_headers())
        rsp.raise_for_status()
        self.soup = BeautifulSoup(rsp.text, features="html.parser")

    def get_product_name(self):
        name_span = self.soup.find("span", {"id": "productTitle"})
        name = name_span.text.strip()
        name = " ".join(name.split())
        return name.split(",")[0]

    def get_price(self) -> float:
        price_span = self.soup.find("span", {"class": "a-price"})
        price = price_span.select("span")[0].text[1:]  # remove currency symbol
        return float(price)
