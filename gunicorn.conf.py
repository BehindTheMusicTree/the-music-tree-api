#!/usr/bin/env python

accesslog = "/var/log/bodzify-api/gunicorn/access.log"
acceslogformat = '%(T)s %(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'