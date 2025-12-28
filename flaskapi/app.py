# pip install -U Flask-SQLAlchemy

from flask import Flask, render_template, flash, redirect, url_for, request
# from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from sqlalchemy import select
from db.base import db
import re
from models.user import User
from models.book import Book
from models.bookarchive import BookArchive
from flask_migrate import Migrate

# create the app
app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///booklibrary.db"

# initialize the app with the extension
db.init_app(app)

migrate = Migrate(app=app, db=db)

# db = SQLAlchemy(app=app)
    
# user_book_m2m = db.Table(
#     "user_book",
#     sa.Column("user_id", sa.ForeignKey(User.id), primary_key=True),
#     sa.Column("book_id", sa.ForeignKey(Book.id), primary_key=True),
# )


@app.route("/")
def load_root():
    users = db.session.execute(db.select(User).order_by(User.name)).scalars().all()
    books = db.session.execute(db.select(Book).order_by(Book.name)).scalars()

    # user1 = users[1]
    # print(users)
    # print(user1.book_archive)
    # print(user1.book_archive.books)
    # print(book_arv)
    # described_books = [item.name for item in book_arv]
    # return render_template("home.html", users = users, described_books = described_books, books = books)

    return render_template("home.html", users = users, books = books)


@app.route("/user/<string:name>")
def load_user(name):
    return render_template("user/user.html", name=name.title())

@app.route("/users", methods=["POST", "GET"])
def load_user_list():
    users = db.session.execute(db.select(User).order_by(User.name)).scalars()
    return render_template("user/list.html", users=enumerate(users))

@app.route("/user/<int:id>/create")
def create_user(id):
    user = db.get_or_404(User, id)
    return render_template("user/detail.html", user=user)

@app.route("/user/<int:id>/detail")
def user_detail(id):
    # user = db.get_or_404(User, id, description=f"User with Id {id} not found!")
    user = User.query.get(id)
    if user is None:
        return render_template("user/detail.html", message=f"User with Id {id} was not found!")
    return render_template("user/detail.html", user=user)

@app.route("/user/<int:id>/update", methods=["POST", "GET"])
def update_user(id):
    user = db.get_or_404(User, id)
    if request.method == "POST":
        try:
            user.name = request.form["name"]
            user.email = request.form["email"]

            db.session.commit()
            return redirect("/users")
        
        except sa.exc.IntegrityError as IE:
            db.session.rollback()
            print(f"Error: Email exists")
            return f"Error: Email exists", 400
        # except Exception as e:
        #     db.session.rollback()
        #     print(f"Error: {e}")
        #     return f"Error: {e}", 400 
    return render_template("user/update.html", user=user)

@app.route("/user/<int:id>/delete")
def delete_user(id):
    user = db.get_or_404(User, id)

    try:
        db.session.delete(user)
        db.session.commit()
        return redirect("/users")
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"

@app.route("/.well-known/appspecific/com.chrome.devtools.json", methods=["GET"])
def use_devtools():
    return render_template("user/user.html", user="Developer")

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404_error.html'), 404

# @app.route("/users/create", methods=["GET", "POST"])
# def user_create():
#     if request.method == "POST":
#         user = User(
#             username=request.form["username"],
#             email=request.form["email"],
#         )
#         db.session.add(user)
#         db.session.commit()
#         return redirect(url_for("user_detail", id=user.id))

#     return render_template("user/create.html")

with app.app_context():
    user_infors = [{"name": "user1", "email": "email1@gmail.com"},
                {"name": "user2", "email": "email2@gmail.com"},
                {"name": "user3", "email": "email3@gmail.com"},
                {"name": "user4", "email": "email4@gmail.com"},
                {"name": "user5", "email": "email5@gmail.com"},
                ]
    book_infors = [{"name": "book1", "author": "author1", "category": "category1", "describe": "describe1", "publication_date": "10.11.2025", "reading_status": "reading"},
                {"name": "book2", "author": "author2", "category": "category2", "describe": "describe2", "publication_date": "11.11.2025", "reading_status": "reading"},
                {"name": "book3", "author": "author3", "category": "category3", "describe": "describe3", "publication_date": "12.11.2025", "reading_status": "reading"},
                {"name": "book4", "author": "author4", "category": "category4", "describe": "describe4", "publication_date": "13.11.2025", "reading_status": "reading"},
                {"name": "book5", "author": "author5", "category": "category5", "describe": "describe5", "publication_date": "14.11.2025", "reading_status": "reading"},
                ]

    try:
        db.drop_all()

        db.create_all()

        for user_inf in user_infors:
            db.session.add(User(**user_inf))
            db.session.commit()

        for book_inf in book_infors:
            db.session.add(Book(**book_inf))
            db.session.commit()

        # AttributeError: 'Select' object has no attribute 'name'
        # user1 = select(User).where(User.id == 1)

        user1 = db.session.execute(db.select(User).order_by(User.id == 1)).scalar()
        books = db.session.execute(db.select(Book).order_by(Book.name)).scalars()

        # print(user1.name, book1.name)

        for book in books:
            user1.add_to_archive(book)

        stmt = (
            select(BookArchive)
            .join(User, BookArchive.user_id == User.id)  # JOIN with true condition
            .order_by(User.name)
        )

        result = db.session.execute(stmt).scalars().all()
    except sa.exc.IntegrityError as IE:
        print("error occurred!")


#     db.create_all()
#     db.session.add(User(username="example"))
#     db.session.commit()

#     users = db.session.execute(db.select(User)).scalars()

# if __name__ == "__main__":
#     app.run("0.0.0.0", 5555)