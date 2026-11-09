import requests


class Post:

    def __init__(self):
        self.url = "https://api.npoint.io/c790b4d5cab58020d391"
        self.raw_json = None
        self.posts = None
        self._get_posts()

    def _get_posts(self):
        rsp = requests.get(self.url)
        rsp.raise_for_status()
        self.raw_json = rsp.json()
        posts = {str(p["id"]): {"title": p["title"], "subtitle": p["subtitle"], "body": p["body"],} for p in rsp.json()}
        self.posts = posts