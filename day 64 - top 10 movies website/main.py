from docutils.nodes import title
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from tmdb_manager import TMDBRequestsManager


tmdb_manager = TMDBRequestsManager()

# Start Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DB
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///top-10-movies.db"
db.init_app(app)

# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    rating: Mapped[float|None] = mapped_column(Float)
    ranking: Mapped[int|None] = mapped_column(Integer)
    review: Mapped[str|None] = mapped_column(String)
    img_url: Mapped[str] = mapped_column(String, nullable=False)

with app.app_context():
    db.create_all()

# Flask forms

class EditMovie(FlaskForm):
    rating = StringField("Your rating out of 10", validators=[DataRequired()])
    review = StringField("Your review", validators=[DataRequired()])
    submit = SubmitField("Done")

class AddMovie(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")

# flask routes

@app.route("/")
def home():
    results = db.session.execute(db.select(Movie).order_by(Movie.rating))
    movies_list = list(results.scalars())
    # assign rankings based on ratings
    for i, movie in enumerate(movies_list):
        movie.ranking = len(movies_list) - i
        db.session.commit()
    return render_template("index.html", movies=movies_list)


@app.route("/edit", methods=['GET', 'POST'])
def edit():
    edit_form = EditMovie()
    movie_id = request.args.get("id")
    movie_to_edit = db.get_or_404(Movie, movie_id)
    if edit_form.validate_on_submit():
        movie_to_edit.rating = float(edit_form.rating.data)
        movie_to_edit.review = edit_form.review.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", form=edit_form, name=movie_to_edit.title)


@app.route("/delete")
def delete():
    movie_id = request.args.get("id")
    print(f"Deleting movie card: {movie_id}")
    db.session.delete(db.get_or_404(Movie, movie_id))
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/add", methods=['GET', 'POST'])
def add():
    add_form = AddMovie()
    # display list of search results
    if add_form.validate_on_submit():
        new_movie_title = add_form.title.data
        search_result = tmdb_manager.search_movie(new_movie_title)
        return render_template("select.html", movies=search_result)
    # after user selects a movie from the select page list
    tmdb_movie_id = request.args.get("id")
    if tmdb_movie_id:
        details = tmdb_manager.get_movie_details(tmdb_movie_id)
        movie_to_add = Movie(
            title=details["title"],
            year=details["release_date"].split("-")[0],
            description=details["overview"],
            img_url=tmdb_manager.get_poster_url(details["poster_path"]),
        )
        db.session.add(movie_to_add)
        db.session.commit()
        return redirect(url_for("edit", id=movie_to_add.id))  # edit always wants an id
    return render_template("add.html", form=add_form)


if __name__ == '__main__':
    app.run(debug=True)