from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pprint import pprint
import requests
import os

from spotipy_manager import SpotipyManager


load_dotenv(".env")
BILLBOARD_MOCK_URL = "https://appbrewery.github.io/bakeboard-hot-100/"
BILLBOARD_REAL_URL = "https://www.billboard.com/charts/hot-100/"


def main():

    # date = input("Which year do you want to travel to? Type the date in YYYY-MM-DD format: ")
    date = "2014-10-18"

    rsp = requests.get(
        url=f"{BILLBOARD_MOCK_URL}{date}/",
        headers={"USER-AGENT": os.getenv("USER_AGENT")},
    )
    rsp.raise_for_status()

    soup = BeautifulSoup(rsp.text, "html.parser")
    entries = soup.find_all(name="h3", class_="chart-entry__title")
    top_100_songs = [tag.text for tag in entries]
    # pprint(top_100_songs)

    # search the top 100 songs in spotify
    sm = SpotipyManager()
    track_uris = []
    for song in top_100_songs:
        # searching just by track name and year might lead to wrong results
        search_query = {
            "track": song,
            "year": date.split("-")[0],
        }
        result = sm.search(search_query, limit=1, market="GB")
        track_name = result["tracks"]["items"][0]["name"]
        artist = result["tracks"]["items"][0]["artists"][0]["name"]
        track_uri = result["tracks"]["items"][0]["uri"]
        track_uris.append(track_uri)
        info = (track_name, artist, track_uri)
        # print(info)

    # create new public playlist
    new_playlist = sm.create_playlist(
        name=f"{date} Billboard 100",
        description="This was made by Python!"
    )

    # add all 100 tracks into it
    sm.add_tracks_to_playlist(new_playlist, track_uris)

    # pprint(sm.get_my_playlists_info(show=["items"]))
    # sm.delete_playlist("4JE0CFWaqRbcFo8QOuHTGY")


if __name__ == '__main__':
    main()
