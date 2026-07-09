import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os


load_dotenv(".env")


class SpotipyManager:

    def __init__(self):
        self.spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.spotify_redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
        self.oauth = None
        self.session = None
        self.playlists = None
        self._initialise()
        self._load_playlists()

    def _create_oauth(self):
        self.oauth = SpotifyOAuth(
            client_id=self.spotify_client_id,
            client_secret=self.spotify_client_secret,
            redirect_uri=self.spotify_redirect_uri,
            scope=[
                "user-library-read",
                "playlist-modify-public",
                "playlist-modify-private",
                "playlist-read-private",
            ]
        )

    def _initialise(self):
        self._create_oauth()
        self.session = spotipy.Spotify(oauth_manager=self.oauth)

    def _load_playlists(self):
        self.playlists = self.session.current_user_playlists()

    def get_my_playlists_info(self, show=None) -> dict:
        if not show:
            show = [
                "id",
                "description",
                "external_urls",
                "items",
            ]
        my_playlists = {
            playlist["name"]: {
                info: playlist[info] for info in show
            } for playlist in self.playlists["items"]
        }
        return my_playlists

    def create_playlist(self, **kwargs) -> str:
        output = self.session.current_user_playlist_create(**kwargs)
        _id = output["id"]
        print(f"\nPlaylist created: {kwargs}\nid: {_id}\n")
        self._load_playlists()
        return _id

    def delete_playlist(self, _id: str):
        confirmation = input(
            f"The playlist with id: {_id} is about to be permanently deleted.\n"
            f"Are you sure? (yes/no): "
        )
        if confirmation.lower() == "yes":
            self.session.current_user_unfollow_playlist(playlist_id=_id)
            self._load_playlists()

    def get_user_id(self) -> str:
        return self.session.current_user()["id"]

    def search(self, query, **kwargs) -> dict:
        query_str = ""
        for key, val in query.items():
            query_str += f"{key}:"
            query_str += val.replace(" ", "+")
            query_str += " "
        # print(query_str)
        result = self.session.search(q=query_str, **kwargs)
        return result

    def add_tracks_to_playlist(self, playlist_id: str, tracks: list):
        self.session.playlist_add_items(playlist_id, tracks)
