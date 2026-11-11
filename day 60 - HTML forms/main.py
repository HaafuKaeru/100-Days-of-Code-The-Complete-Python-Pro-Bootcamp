from flask import Flask, render_template, request
import requests
import smtplib
import os
import dotenv


dotenv.load_dotenv("../.env")
SMTP_ADDRESS = os.getenv("smtp_address")
SERVER_EMAIL = os.getenv("my_email")
CLIENT_EMAIL = os.getenv("my_test_email")
CLIENT_EMAIL_PASS = os.getenv("my_test_email_pass")


def send_email(name=None, email=None, phone=None, message=None):
    if email == CLIENT_EMAIL:  # only use the test email address for this
        with smtplib.SMTP(SMTP_ADDRESS) as connection:
            connection.starttls()
            connection.login(user=CLIENT_EMAIL, password=CLIENT_EMAIL_PASS)
            connection.sendmail(
                from_addr=CLIENT_EMAIL,
                to_addrs=SERVER_EMAIL,
                msg=f"Subject: New message\n\n"
                    f"Name: {name}\n"
                    f"Email: {email}\n"
                    f"Phone: {phone}\n"
                    f"Message: {message}"
            )


# USE YOUR OWN npoint LINK! ADD AN IMAGE URL FOR YOUR POST. 👇
posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        send_email(**request.form)
        return render_template("contact.html", heading="Successfully sent message")
    return render_template("contact.html", heading="Contact me")


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
