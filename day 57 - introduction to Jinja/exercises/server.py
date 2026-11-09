from flask import Flask, render_template
from datetime import datetime
import requests
import requests_cache
import json


GENDERIZE_API_URL = "https://api.genderize.io"
AGIFY_API_URL = "https://api.agify.io"

requests_cache.install_cache("fake_blogs")


def get_gender_and_age(name: str) -> dict:
    params = {
        "name": name,
    }
    gender  = requests.get(GENDERIZE_API_URL, params=params)
    gender.raise_for_status()
    gender = json.loads(gender.json())
    age = requests.get(AGIFY_API_URL, params=params)
    age.raise_for_status()
    age = json.loads(age.json())
    result = gender.update(age)
    result["name"] = name.title()
    return result


app = Flask(__name__)

@app.route("/")
def home():
    current_year = datetime.now().year
    kwargs = {
        "year": current_year,
    }
    return render_template("index.html", **kwargs)


@app.route("/guess/<input_name>")
def guess(input_name: str):
    result = get_gender_and_age(input_name)
    return render_template("guess.html", **result)


@app.route("/blog/<num>")
def get_blog(num):
    blog_url = "https://api.npoint.io/c790b4d5cab58020d391"
    rsp = requests.get(blog_url)
    rsp.raise_for_status()
    all_posts = rsp.json()
    return render_template("blog.html", posts=all_posts)


if __name__ == '__main__':
    app.run(debug=True)