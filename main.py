from flask import Flask, render_template
from database import Database
import sqlite3

app = Flask(__name__)
db_connection = sqlite3.connect("database.db", check_same_thread=False)
db = Database(db_connection)

db.make_posts_from_md()

@app.route('/')
def home():
    return render_template("home.html", posts=db.get_posts())


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.route("/about")
def about():
    return "under construction"


@app.route("/post/<int:post_id>")
def post(post_id):
    post = db.get_post(post_id)

    if "error" in post:
        return render_template('404.html'), 404

    return render_template("post.html", post=post, posts=db.get_posts())


app.run(host='0.0.0.0', port=81)
