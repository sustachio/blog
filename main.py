from flask import Flask, render_template, request, redirect, url_for
from database import Database, get_visits, increment_visits
import moderation
import css_maker
import sqlite3
import doughnut
import datetime

app = Flask(__name__)

# used to add to a page after it has been rendered
def page_wrapper(page):    
    return render_template(
        "head.html",    # wrapper template
        body= (
            doughnut.generate_html(page)
                if request.args.get("doughnut") != None
                else page
        ),
        extra_css = (    # make random css if random_css
            css_maker.generate_css(page) 
                if request.args.get("random_css") != None
                else ""
        ) + (            # needed css for doughnut text
            "*{white-space: pre-wrap;font-family: monospace;}"
                if request.args.get("doughnut") != None
                else ""
        )
    )

###### DATABASE ######

db_connection = sqlite3.connect("database.db", check_same_thread=False)
db = Database(db_connection)
#db.update_tables()

###### MODERATION ######

moderation.start_up(db)
#moderation.validate_all_comments()

###### STATIC PAGES ######

@app.route('/')
def home():
    increment_visits()

    time = datetime.datetime.now()

    holiday = "holiday-none"
    if (time.month == 12 and time.day <= 25): holiday = "holiday-christmas"
    if (time.month == 10 and time.day == 31): holiday = "holiday-halloween"
    if (time.month == 1  and time.day == 1 ): holiday = "holiday-newyears"
    if (time.month == 2  and time.day == 14): holiday = "holiday-valentines"
    if (time.month == 7  and time.day == 4 ): holiday = "holiday-fourth"

    return page_wrapper(
        render_template(
            "home.html", 
            posts=db.get_posts(),
            visits=get_visits(),
            holiday=holiday
        ))

@app.errorhandler(404)
@app.route("/404")
def page_not_found(_=None):
    return page_wrapper(
            render_template(
            "404.html",
            posts=db.get_posts(),
        )
    ), 404

@app.route("/portfolio")
def portfolio():
    return page_wrapper(
        render_template(
            "portfolio.html",
            posts=db.get_posts()
        )
    )

@app.route("/projects")
def projects():
    return page_wrapper(
        render_template(
            "home.html", 
            all_posts=db.get_posts(), 
            posts=db.get_projects(),
            visits=get_visits()
        )
    )

@app.route("/findme")
def find_me():
    return page_wrapper(
        render_template(
            "find me.html", 
            posts=db.get_posts(),
            all_posts=db.get_posts(), 
        )
    )

@app.route("/spm")
def strokes_per_minute_counter():
    return render_template("spm_counter.html")

###### QUERIED PAGES ######

@app.route("/post/<post_id>")
def post(post_id):
    post = db.get_post(post_id)

    if post == "error":
        return redirect(url_for("page_not_found"))

    alert = request.args.get("alert", "")

    return page_wrapper(
        render_template(
            "post.html", 
            post=post, 
            posts=db.get_posts(),
            all_posts=db.get_posts(),
            comments=db.get_comments(post_id),
            alert=alert
        )
    )

###### APIS ######

@app.route("/post_comment/<post_id>", methods=["POST"])
def post_comment(post_id):
    if len(request.form.get("comment")) > 1500: 
        return redirect(url_for("post", post_id=post_id, alert="Comment too long (>1500 chars)"))

    if len(request.form.get("name")) > 100: 
        return redirect(url_for("post", post_id=post_id, alert="Name too long (>100 chars)"))

    db.add_comment(post_id, request.form.get("name"), request.form.get("comment"))

    return redirect(url_for("post", post_id=post_id))

###################

db.make_posts_from_md(app)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81)
