from flask import Flask, render_template
import requests


NPOINT_API_URL = "https://api.npoint.io/b708ff4bc2bc1d9f439a"


def get_posts_content() -> list[dict]:
    rsp = requests.get(NPOINT_API_URL)
    rsp.raise_for_status()
    # print(rsp.json())
    return rsp.json()


raw_posts_data = get_posts_content()
clean_posts_data = {
    post['id']: {
        "body": post["body"],
        "title": post["title"],
        "subtitle": post["subtitle"],
    } for post in raw_posts_data
}

app = Flask(__name__)

@app.route("/")
def home():
    data = {
        "page": "home",
        "heading": "Haafu Kaeru's Blog",
        "subheading": "A collection of random blogs to practice Bootstrap",
        "posts": raw_posts_data,
        "author": "Haafu Kaeru",
        "date": "10th November, 2026",
    }
    return render_template("index.html", **data)

@app.route("/about")
def about():
    heading = "About Me"
    subheading = "This is what I do."
    return render_template("about.html", heading=heading, subheading=subheading, page="about")

@app.route("/contact")
def contact():
    heading = "Contact Me"
    subheading = "Have questions? I have answers."
    return render_template("contact.html", heading=heading, subheading=subheading, page="contact")

@app.route("/post/<int:_id>")
def post_page(_id: int):
    data = {
        "content": clean_posts_data[_id],
        "author": "Haafu Kaeru",
        "date": "10th November, 2026",
    }
    return render_template("post.html", _id=_id, **data)


if __name__ == '__main__':
    get_posts_content()
    app.run(debug=True)