from os import listdir
from markdown import markdown

class Database():
    def __init__(self, connection):
        self.db = connection
        self.db_cursor = self.db.cursor()
    
    def add_post(self, post):
        # make sure the post doesent already exist
        self.db_cursor.execute("SELECT * FROM posts WHERE title=?", (post["title"],))
        if self.db_cursor.fetchall():
            self.db_cursor.execute("""UPDATE posts
                          SET posted_on=?, content=?, post_id=?
                          WHERE title=?""",
                          (post["date"], post["content"], post["id"],
                          post["title"]))
    
            self.db.commit()
    
            return
    
        self.db_cursor.execute("""INSERT INTO posts
                      VALUES(?,?,?,?)""",
                      (post["id"], post["title"], post["date"], post["content"]))
        self.db.commit()
    
    def make_posts_from_md(self):
        for file in listdir("posts_md/"):
            # convert md to html
            with open("posts_md/" + file, "r") as f:
                (title, date, *content) = f.readlines()
    
                content = markdown("\n".join(content))
    
            self.db_cursor.execute("SELECT * FROM posts")
            id = len(self.db_cursor.fetchone())
    
            self.add_post({
                "title": title,
                "date": date,
                "id": id,
                "content": content
            })
        
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
    
    def get_post(self, post_id):
        self.db_cursor.execute("SELECT * FROM posts WHERE post_id=?",(post_id,))
        post = self.db_cursor.fetchone()
    
        return {
            "id": post[0],
            "title": post[1],
            "date": post[2],
            "content": post[3]
        }