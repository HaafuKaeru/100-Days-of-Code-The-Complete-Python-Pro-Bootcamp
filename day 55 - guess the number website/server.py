from flask import Flask
from random import randint


app = Flask(__name__)
number = randint(0, 9)


@app.route("/<int:user_number>")
def guess_number(user_number: int):
    html = ""
    if user_number < number:
        html = "<h1 style='color:red'>Too low, try again!</h1>"
        gif = "https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif"
    elif user_number > number:
        html = "<h1 style='color:purple'>Too high, try again!</h1>"
        gif = "https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif"
    elif user_number == number:
        html = "<h1 style='color:green'>You found me!</h1>"
        gif = "https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif"
    html += f"<img src='{gif}'></img>"
    return html


@app.route("/")
def home():
    html = "<h1>Guess a number between 0 and 9</h1>"
    start_gif = "https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif"
    html += f"<img src={start_gif}></img>"
    return html


if __name__ == '__main__':
    app.run(debug=True)