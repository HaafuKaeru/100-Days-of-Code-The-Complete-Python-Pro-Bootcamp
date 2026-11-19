from flask import Flask


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def make_bold(func):
    def wrapper():
        return '<b>' + func() + '</b>'
    return wrapper

def make_emphasis(func):
    def wrapper():
        return '<em>' + func() + '</em>'
    return wrapper

def make_underlined(func):
    def wrapper():
        return '<u>' + func() + '</u>'
    return wrapper



@app.route("/bye")
@make_bold
@make_emphasis
@make_underlined
def say_bye():
    return "Bye!"

# @app.route("/user/<name>/<int:number>")
# def greetings(name: str, number: int):
#     return f"Hello there, {name} the number is {number}!"


if __name__ == "__main__":
    app.run(debug=True)