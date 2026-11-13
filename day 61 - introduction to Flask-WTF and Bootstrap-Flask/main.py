from flask import Flask, render_template
from flask_wtf import FlaskForm
from scipy.stats import bootstrap
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length
from flask_bootstrap import Bootstrap4


'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt
'''


app = Flask(__name__)
app.secret_key = "itsmemario"
bootstrap = Bootstrap4(app)


class LoginForm(FlaskForm):
    email = EmailField(label='Email', validators=[InputRequired(), Email(), Length(min=8)])
    password = PasswordField(label='Password', validators=[InputRequired()])
    submit = SubmitField(label="Log In")


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login", methods=['POST', 'GET'])
def login():
    secret_email = "admin@email.com"
    secret_pass = "12345678"
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if login_form.email.data == secret_email and login_form.password.data == secret_pass:
            return render_template("success.html")
        else:
            return render_template("denied.html")
    return render_template("login.html", form=login_form)


# @app.route("/success")
# def success():


if __name__ == '__main__':
    app.run(debug=True)
