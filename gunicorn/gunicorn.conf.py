workers = 4
bind = "0.0.0.0:8000"
accessLog="/var/log/gunicorn/access.log"
errorLog="/var/log/gunicorn/error.log"
loglevel="info"