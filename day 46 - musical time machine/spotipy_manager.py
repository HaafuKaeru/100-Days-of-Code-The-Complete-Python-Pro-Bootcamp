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
        self._initialise()

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