from flask import Flask, render_template, request, redirect, url_for
from database import Database
import sqlite3

app = Flask(__name__)
db_connection = sqlite3.connect("database.db", check_same_thread=False)
db = Database(db_connection)

db.make_posts_from_md()

@app.route('/')
def home():
    return render_template("home.html", all_posts=db.get_posts(), posts=db.get_posts())

@app.route("/projects")
def projects():
    return render_template("home.html", all_posts=db.get_posts(), posts=db.get_projects())

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.route("/about")
def about():
    return "under construction"

@app.route("/findme")
def find_me():
    return render_template("find me.html", posts=db.get_posts())

@app.route("/post/<int:post_id>")
def post(post_id):
    post = db.get_post(post_id)

    if "error" in post:
        return render_template('404.html'), 404

    return render_template("post.html", post=post, posts=db.get_posts(), comments=db.get_comments(post_id))

@app.route("/post_comment/<int:post_id>", methods=["POST"])
def post_comment(post_id):
    print("fetched")
    db.add_comment(post_id, request.form.get("name"), request.form.get("comment"))

    return redirect(url_for("post", post_id=post_id))
    
    

app.run(host='0.0.0.0', port=81)
