from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, URL
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):

    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField("Cafe Location on Google Maps (URL)", validators=[DataRequired(), URL()])
    open_time = StringField("Opening Time e.g. 8AM", validators=[DataRequired()])
    close_time = StringField("Closing Time e.g. 5:30PM", validators=[DataRequired()])

    coffee_rating_choices = ["☕️" + i*"☕️" for i in range(5)]
    coffee_rating = SelectField("Coffee Rating", choices=coffee_rating_choices, validators=[DataRequired()])
    wifi_rating_choices = ["💪" + i*"💪" for i in range(5)]
    wifi_rating = SelectField("WiFi Strength Rating", choices=["✘", *wifi_rating_choices], validators=[DataRequired()])
    sockets_rating_choices = ["🔌" + i*"🔌" for i in range(5)]
    sockets_rating = SelectField("Power Sockets Availability", choices=["✘", *sockets_rating_choices], validators=[DataRequired()])

    submit = SubmitField('Submit')


# all Flask routes below


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("Adding new data")
        with open("cafe-data.csv", mode='a', encoding='utf-8') as file:
            values_list = list(form.data.values())
            file.writelines(",".join(values_list[:-2]))
        return cafes()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)