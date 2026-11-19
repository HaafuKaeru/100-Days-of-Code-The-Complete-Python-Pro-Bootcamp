from flask import Flask, render_template
from post import Post


app = Flask(__name__)
post = Post()
raw_json = post.raw_json
# print(raw_json)


@app.route('/')
def home():
    return render_template("index.html", posts=raw_json)


@app.route("/post/<post_id>")
def post_page(post_id: str):
    return render_template("post.html", **post.posts[post_id])


if __name__ == "__main__":
    app.run(debug=True)
