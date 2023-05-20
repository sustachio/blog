from os import listdir
from markdown import markdown
import time
from re import sub
from flask import render_template_string
from json import loads, dumps
import moderation

def get_visits():
    with open("stats.json", "r") as f:
        stats = loads(f.read())

    return stats["visits"]

def increment_visits():
    with open("stats.json", "r") as f:
        stats = loads(f.read())

    stats["visits"] += 1

    with open("stats.json", "w") as f:
        f.write(dumps(stats))


class Database():
    def __init__(self, connection):
        self.db = connection
        self.db_cursor = self.db.cursor()

    
    # create the tables for this database
    # WARNING: ERASES ALL CURRENT DATA
    def make_tables(self):
        try:
            self.db_cursor.execute("DROP TABLE posts")
            self.db_cursor.execute("DROP TABLE comments")
        except:
            pass

        self.db_cursor.execute("""CREATE TABLE posts (
            post_id text PRIMARY KEY NOT NULL,
            title text,
            type text,
            posted_on date,
            content text
        )""")
        
        self.db_cursor.execute("""CREATE TABLE comments (
            comment_id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
            post_id text,
            user_name text,
            posted_on date,
            content text,
            public tinyint,
            replying_to int DEFAULT 0
        )""")     

        self.db.commit()

    def update_tables(self):
        #self.db_cursor.execute("ALTER TABLE comments ADD COLUMN public TINYINT")
        #self.db_cursor.execute("UPDATE comments SET public=0")
        # self.db_cursor.execute("ALTER TABLE comments ADD COLUMN replying_to INT")
        # self.db_cursor.execute("UPDATE comments SET replying_to=0")
        #self.add_comment("a-blog-post-about-this-blog", "Seth M", "Test reply comment", replying_to=3)
        #self.db.commit()
        return
    
    ###### POSTS ######

    
    def make_posts_from_md(self, app):
        # delete old data
        self.db_cursor.execute("DELETE FROM posts")
        self.db.commit()

        for file in listdir("posts_md/"):
            # read md rendering jinja
            with app.app_context(), app.test_request_context(), open("posts_md/"+file, "r") as f:
                text = render_template_string(f.read())
                
            # convert md to html
            (title, type, date, *content) = text.split("\n")

            content = markdown("\n".join(content))
            type = type.strip()
            date = date.strip()
            title = title.strip()
        
            self.add_post_to_db({
                "title": title,
                "type": type,
                "date": date,
                "content": content
            })

    
    def add_post_to_db(self, post):
        # replace non-url charecters with -
        id = sub(r"[^0-9a-zA-Z]+", '-', post["title"].lower().strip())
        
        self.db_cursor.execute("""INSERT INTO posts
                  VALUES(?,?,?,?,?)""",
                  (id, post["title"],  post["type"], post["date"], post["content"]))
        
        self.db.commit()

    
    def get_post(self, post_id):
        self.db_cursor.execute("SELECT * FROM posts WHERE post_id=?",(post_id,))
        post = self.db_cursor.fetchone()

        if not post:
            return "error"
    
        return {
            "id": post[0],
            "title": post[1],
            "type": post[2],
            "date": post[3],
            "content": post[4]
        }

    
    def get_posts(self):
        self.db_cursor.execute("SELECT * FROM posts ORDER BY posted_on")
        posts = [
            {
                "id": post[0],
                "title": post[1],
                "type": post[2],
                "date": post[3],
                "content": post[4]
            }
            for post in self.db_cursor.fetchall()
        ]
    
        return posts

    
    def get_projects(self):
        self.db_cursor.execute('SELECT * FROM posts WHERE type=? ORDER BY posted_on', ("Project",))
        posts = [
            {
                "id": post[0],
                "title": post[1],
                "type": post[2],
                "date": post[3],
                "content": post[4]
            }
            for post in self.db_cursor.fetchall()
        ]
    
        return posts

    
    ###### COMMENTS ######

    
    def add_comment(self, post_id, user_name, content, replying_to=0):
        self.db_cursor.execute("SELECT * FROM comments")

        posted_on = time.strftime('%Y-%m-%d')
        
        self.db_cursor.execute("INSERT INTO comments VALUES(?,?,?,?,?,0,?)",
                              (None, post_id, user_name, posted_on, content, replying_to))

        self.db.commit()

        # validate it
        self.db_cursor.execute("SELECT last_insert_rowid()")
        moderation.validate_comment(self.db_cursor.fetchone()[0])

    def get_comment(self, comment_id):
        self.db_cursor.execute("SELECT * FROM comments WHERE comment_id=?",(comment_id,))
        comment = self.db_cursor.fetchone()

        if not comment:
            return "error"
    
        return {
            "comment_id": comment[0],
            "post_id": comment[1],
            "user_name": comment[2],
            "posted_on": comment[3],
            "content": comment[4],
            "public": comment[5]
        }
    
    def delete_comment(self, comment_id):
        self.db_cursor.execute("DELTE FROM comments WHERE comment_id=?", (comment_id,))
        self.db.commit()
        

    def get_comments(self, post_id, replying_to=0):
        self.db_cursor.execute("SELECT * FROM comments WHERE ((post_id=? AND replying_to=?) AND public=1) ORDER BY posted_on", (post_id,replying_to))
        
        return [{
            "comment_id": comment[0],
            "post_id": comment[1],
            "user_name": comment[2],
            "posted_on": comment[3],
            "content": comment[4],
            "public": comment[5],
            "replies": self.get_comments(post_id, replying_to=comment[0]),
        } for comment in self.db_cursor.fetchall()]

    def get_all_comments(self):
        self.db_cursor.execute("SELECT * FROM comments WHERE replying_to=0 ORDER BY posted_on")

        return [{
            "comment_id": comment[0],
            "post_id": comment[1],
            "user_name": comment[2],
            "posted_on": comment[3],
            "content": comment[4],
            "public": comment[5],
            "replying_to": comment[6],
        } for comment in self.db_cursor.fetchall()]