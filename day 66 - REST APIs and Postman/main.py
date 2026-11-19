from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy.sql.expression import func
from dataclasses import asdict
from http_messages import *


app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase, MappedAsDataclass):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, init=False)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random")
def get_random_cafe():
    result = db.session.execute(db.select(Cafe).order_by(func.random()).limit(1))
    random_cafe = result.scalar()
    return jsonify(asdict(random_cafe))


@app.route("/all")
def get_all_cafes():
    result = db.session.execute(db.select(Cafe))
    all_cafes = list(result.scalars())
    return jsonify(all_cafes)


@app.route("/search")
def get_cafe():
    location = request.args.get("loc")
    result = db.session.execute(db.select(Cafe).where(Cafe.location == location))
    cafes_found = list(result.scalars())
    if not cafes_found:
        err_msg = {
            "error": {
                "Not Found": "Sorry, we don't have a cafe at that location."
            }
        }
        return jsonify(err_msg)
    return jsonify(cafes_found)


# HTTP POST - Create Record
@app.route("/add", methods=['POST'])
def post_new_cafe():
    new_cafe = Cafe(
        name = request.form.get("name"),
        map_url = request.form.get("map_url"),
        img_url = request.form.get("img_url"),
        location = request.form.get("location"),
        seats = request.form.get("seats"),
        has_toilet = bool(request.form.get("toilet")),
        has_wifi = bool(request.form.get("wifi")),
        has_sockets = bool(request.form.get("sockets")),
        can_take_calls = bool(request.form.get("can_take_calls")),
        coffee_price = request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": NEW_CAFE_ADDED})


# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>", methods=['PATCH'])
def update_cafe_price(cafe_id: int):
    try:
        cafe = db.session.get(Cafe, cafe_id)
        new_price = request.args["new_price"]
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": COFFEE_PRICE_UPDATED}), 200
    except AttributeError:
        return jsonify(error={"not found": NO_CAFE_ID}), 404
    except KeyError as e:
        return jsonify(error={"unknown key": WRONG_KEY}), 404


# HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>", methods=['DELETE'])
def delete_cafe(cafe_id: int):
    try:
        cafe = db.session.get(Cafe, cafe_id)
        user_key = request.args["api-key"]
        if user_key != "TopSecretAPIKey":
            return jsonify(error={"unauthorised": WRONG_API_KEY})
        db.session.delete(cafe)
        db.session.commit()
        return jsonify(response={"success": CAFE_DELETED})
    except (AttributeError, UnmappedInstanceError):
        return jsonify(error={"not found": NO_CAFE_ID}), 404
    except KeyError as e:
        return jsonify(error={"unknown key": WRONG_KEY}), 404


if __name__ == '__main__':
    app.run(debug=True)