from IPython.core.release import author
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# create sqlite db
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my-books-collection.db"

db.init_app(app)

# create db model
class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

with app.app_context():
    db.create_all()


# flask routes
@app.route('/')
def home():
    delete_id = request.args.get("id")
    if delete_id:
        print(f"Deleting book")
        book = db.get_or_404(Book, delete_id)
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for("home"))
    result = db.session.execute(db.select(Book).order_by(Book.title))
    list_obj = list(result.scalars())
    return render_template("index.html", books=list_obj)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        book = Book(
            title = request.form["title"],
            author = request.form["author"],
            rating = request.form["rating"]
        )
        db.session.add(book)
        db.session.commit()
        print(f"Book added: {book.title}")
        return redirect(url_for("home"))
    return render_template("add.html")


@app.route("/edit", methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        new_rating = request.form["new_rating"]
        book = db.get_or_404(Book, request.form["id"])
        book.rating = float(new_rating)
        db.session.commit()
        return redirect(url_for("home"))
    book_id = request.args.get("id")
    book = db.get_or_404(Book, book_id)
    return render_template("edit.html", book=book)


if __name__ == "__main__":
    app.run(debug=True)