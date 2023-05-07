line="*/1 * * * * git -C /home/seth/blog pull origin main"
(crontab -u $(whoami) -l; echo "$line" ) | crontab -u $(whoami) -

# pip install flask markdown bs4
# pip install gunicorn greenlet gevent
# sudo gunicorn -k gevent -b 127.0.0.1:4000 main:app
