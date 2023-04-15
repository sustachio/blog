from os import listdir
from markdown import markdown
import time

class Database():
    def __init__(self, connection):
        self.db = connection
        self.db_cursor = self.db.cursor()

    def make_tables(self):
        self.db_cursor.execute("""CREATE TABLE posts (
            post_id integer,
            title text,
            posted_on date,
            content text
        )""")

        self.db_cursor.execute("""CREATE TABLE comments (
            parent_post_id integer,
            comment_id integer,
            user_name text,
            posted_on date,
            content text
        )""")       

    def make_posts_from_md(self):
        # delete old data
        self.db_cursor.execute("DELETE FROM posts")
        self.db.commit()
        
        for file in listdir("posts_md/"):
            # convert md to html
            with open("posts_md/" + file, "r") as f:
                (title, date, *content) = f.readlines()
    
                content = markdown("\n".join(content))
    
            self.db_cursor.execute("SELECT * FROM posts")
            id = len(self.db_cursor.fetchall())
    
            self.add_post({
                "title": title,
                "date": date,
                "id": id,
                "content": content
            })
            
    def add_post(self, post):
        # make sure the post doesent already exist
        self.db_cursor.execute("SELECT * FROM posts WHERE title=?", (post["title"],))
        if self.db_cursor.fetchall():
            self.db_cursor.execute("""UPDATE posts
                          SET posted_on=?, content=?, post_id=?
                          WHERE title=?""",
                          (post["date"], post["content"], post["id"],
                          post["title"]))
    
        else:    
            self.db_cursor.execute("""INSERT INTO posts
                          VALUES(?,?,?,?)""",
                          (post["id"], post["title"], post["date"], post["content"]))
            
        self.db.commit()

    def get_post(self, post_id):
        self.db_cursor.execute("SELECT * FROM posts WHERE post_id=?",(post_id,))
        post = self.db_cursor.fetchone()
    
        return {
            "id": post[0],
            "title": post[1],
            "date": post[2],
            "content": post[3]
        }

    
    def get_posts(self):
        self.db_cursor.execute("SELECT * FROM posts")
        posts = [
            {
                "id": post[0],
                "title": post[1],
                "date": post[2],
                "content": post[3]
            }
            for post in self.db_cursor.fetchall()
        ]
    
        return posts
    

    def add_comment(self, post_id, user_name, content):
        self.db_cursor.execute("SELECT * FROM comments")
        comment_id = len(self.db_cursor.fetchall())

        posted_on = time.strftime('%Y-%m-%d')
        
        self.db_cursor.execute("INSERT INTO comments VALUES(?,?,?,?,?)",
                              (post_id, comment_id, user_name, posted_on, content))

        self.db.commit()

    def delete_comment(self, comment_id):
        self.db_cursor.execute("DELTE FROM comments WHERE comment_id=?", (comment_id,))
        self.db.commit()

    def get_comments(self, post_id):
        self.db_cursor.execute("SELECT * FROM comments WHERE parent_post_id=?", (post_id,))

        return [{
            "parent_post_id": comment[0],
            "comment_id": comment[1],
            "user_name": comment[2],
            "posted_on": comment[3],
            "content": comment[4]
        } for comment in self.db_cursor.fetchall()]