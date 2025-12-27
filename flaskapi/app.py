# pip install -U Flask-SQLAlchemy

from flask import Flask, render_template, flash, redirect, url_for, request
# from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from db.base import db
import re
from models.user import User
from models.book import Book

# create the app
app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///booklibrary.db"

# initialize the app with the extension
db.init_app(app)

# db = SQLAlchemy(app=app)
    
# user_book_m2m = db.Table(
#     "user_book",
#     sa.Column("user_id", sa.ForeignKey(User.id), primary_key=True),
#     sa.Column("book_id", sa.ForeignKey(Book.id), primary_key=True),
# )


@app.route("/")
def load_root():
    return render_template("home.html")

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
    return render_template("user/detail.html", user="I now that you are using the devtools")

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

    try:
        db.create_all()
        for user in user_infors:
            db.session.add(User(**user))
            db.session.commit()
    except Exception as e:
        pass

#     db.create_all()
#     db.session.add(User(username="example"))
#     db.session.commit()

#     users = db.session.execute(db.select(User)).scalars()

# if __name__ == "__main__":
#     app.run("0.0.0.0", 5555)