from flask import Flask, render_template
from os import listdir, remove
from json import loads, dumps
from markdown import markdown

app = Flask(__name__)

post_cataloug = {}


# generate the post catalouge and make the jsons to render the html
def make_posts_from_md():
    post_cataloug = {}

    # wipe old
    for file in listdir("posts"):
        remove("posts/" + file)

    for file in listdir("posts_md/"):
        # text before .md
        file_name = file.split(".")[0]

        # convert md to html
        with open("posts_md/" + file, "r") as f:
            (title, date, *content) = f.readlines()

            content = markdown("\n".join(content))

        id = len(listdir("posts/")) + 1

        # create the json
        with open("posts/" + file_name + ".json", "w") as f:
            f.write(
                dumps({
                    "title": title,
                    "date": date,
                    "id": id,
                    "content": content
                }))

        # update the cataloug
        post_cataloug[str(id)] = file_name + ".json"

    with open("post_cataloug.json", "w") as f:
        f.write(dumps(post_cataloug))


make_posts_from_md()
#with open("post_cataloug.json","r") as f:post_cataloug = loads(f.read())


def get_posts(limit=100):
    posts = []

    for i, file_name in enumerate(listdir("./posts/")):
        with open("./posts/" + file_name, "r") as f:
            posts.append(loads(f.read()))

        if i + 1 > limit:
            break

    return posts


def get_post(post_id):
    post_id = str(post_id)

    with open("post_cataloug.json") as f:
        post_cataloug = loads(f.read())

    if not post_id in post_cataloug:
        return {"error": "404"}

    with open("./posts/" + post_cataloug[post_id]) as f:
        post = loads(f.read())

    return post


@app.route('/')
def home():
    return render_template("home.html", posts=get_posts())


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.route("/about")
def about():
    return "under construction"


@app.route("/post/<int:post_id>")
def post(post_id):
    post = get_post(post_id)

    if "error" in post:
        return render_template('404.html'), 404

    return render_template("post.html", post=post, posts=get_posts())


make_posts_from_md()

app.run(host='0.0.0.0', port=81)
