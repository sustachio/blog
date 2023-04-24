from flask import Flask, render_template, request, redirect, url_for
from database import Database
from css_maker import generate_css
import sqlite3

app = Flask(__name__)
db_connection = sqlite3.connect("database.db", check_same_thread=False)
db = Database(db_connection)

random_css = lambda html : (
    generate_css(html) 
        if request.args.get("random_css") 
        else None
)

@app.route('/')
def home():
    page = render_template(
            "home.html", 
            posts=db.get_posts()
        )
    return render_template(
            "head.html",
            body=page,
            extra_css=random_css(page)
        )

@app.route("/projects")
def projects():
    page = render_template(
        "home.html", 
        all_posts=db.get_posts(), 
        posts=db.get_projects(),
    )
    return render_template(
        "head.html",
        body=page,
        extra_css=random_css(page)
    )

@app.errorhandler(404)
@app.route("/404")
def page_not_found(_=None):
    page = render_template(
        "404.html",
        posts=db.get_posts(),
    )
    return render_template(
        "head.html",
        body=page,
        extra_css=random_css(page)
    ), 404

@app.route("/about")
def about():
    return "under construction"

@app.route("/findme")
def find_me():
    page = render_template(
        "find me.html", 
        posts=db.get_posts(),
        all_posts=db.get_posts(), 
    )
    return render_template(
        "head.html",
        body=page,
        extra_css=random_css(page)
    )

@app.route("/post/<post_id>")
def post(post_id):
    post = db.get_post(post_id)

    if post == "error":
        return redirect(url_for("page_not_found"))

    page = render_template(
        "post.html", 
        post=post, 
        posts=db.get_posts(),
        all_posts=db.get_posts(),
        comments=db.get_comments(post_id),
    )
    return render_template(
        "head.html",
        body=page,
        extra_css=random_css(page)
    )

@app.route("/post_comment/<post_id>", methods=["POST"])
def post_comment(post_id):
    print("fetched")
    db.add_comment(post_id, request.form.get("name"), request.form.get("comment"))

    return redirect(url_for("post", post_id=post_id))
    
db.make_posts_from_md(app)

app.run(host='0.0.0.0', port=81)
