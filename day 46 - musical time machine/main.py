import requests
from bs4 import BeautifulSoup
from pprint import pprint
from dotenv import load_dotenv
import os


load_dotenv(".env")
BASE_URL = "https://appbrewery.github.io/bakeboard-hot-100/"


def main():

    # user_input = input("Which year do you want to travel to? Type the date in YYYY-MM-DD format: ")
    user_input = "2014-10-18"

    headers = {
        "USER-AGENT": os.getenv("USER-AGENT")
    }

    rsp = requests.get(
        url=f"{BASE_URL}{user_input}/",
        headers=headers,
    )
    rsp.raise_for_status()

    soup = BeautifulSoup(rsp.text, "html.parser")
    entries = soup.find_all(name="h3", class_="chart-entry__title")
    top_100_songs = [tag.text for tag in entries]
    # print(top_100_songs)

    # user_id = sp.current_user()["id"]
    # print(user_id)
    # sp.current_user_playlist_create(name="Test", description="this was created by Python")
    # pprint(sp.current_user_playlists())
    # sp.current_user_unfollow_playlist(playlist_id="xxx")
    my_playlists = {playlist["name"]: playlist["id"] for playlist in sp.current_user_playlists()["items"]}
    pprint(my_playlists)


if __name__ == '__main__':
    main()
