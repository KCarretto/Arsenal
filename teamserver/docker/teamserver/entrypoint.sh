#!/bin/sh

cd /opt/arsenal/
uwsgi --ini uwsgi.ini --lazy-apps --daemonize /var/log/arsenal.log
nginx -g "daemon off;"
