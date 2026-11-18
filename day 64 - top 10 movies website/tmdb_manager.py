import requests
import os
import dotenv


dotenv.load_dotenv("../.env")

TMDB_BEARER_TOKEN = os.getenv("tmdb_api_bearer_token")
TMDB_API_KEY = os.getenv("tmdb_api_key")
TMDB_API_BASE_URL = "https://api.themoviedb.org/3"


class TMDBRequestsManager:

    def __init__(self):
        self.base_url = TMDB_API_BASE_URL
        self.bearer_token = TMDB_BEARER_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.bearer_token}"
        }

    def search_movie(self, movie_name: str) -> list[dict]:
        query = {
            "query": movie_name
        }
        rsp = requests.get(self.base_url + "/search/movie", params=query, headers=self.headers)
        rsp.raise_for_status()
        results_list = rsp.json()["results"]
        return results_list

    def get_movie_details(self, movie_id: str) -> dict:
        rsp = requests.get(self.base_url + f"/movie/{movie_id}", headers=self.headers)
        rsp.raise_for_status()
        return rsp.json()

    def get_poster_url(self, img_path: str, size="w500") -> str:
        conf_rsp = requests.get(self.base_url + "/configuration", headers=self.headers)
        conf_rsp.raise_for_status()
        configuration = conf_rsp.json()
        base_url = configuration["images"]["secure_base_url"]
        img_size = size
        return base_url + img_size + img_path