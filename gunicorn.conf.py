from glob import glob

# sudo gunicorn -c /home/seth/blog/gunicorn.conf.py

chdir = "/home/seth/blog"

wsgi_app = "main:app"
bind = "0.0.0.0:8443"
worker_class = "gevent"
timeout = 60

reload = True
reload_extra_files = glob("/home/seth/blog/templates/*") + glob("/home/seth/blog/posts_md/*") + glob("/home/seth/blog/static/*") + glob("/home/seth/blog/*.py")

certfile = "/home/seth/blog/fullchain.pem"
keyfile = "/home/seth/blog/privkey.pem"
