#!/bin/sh

cd /opt/arsenal/
celery multi start 5 --app=teamserver.events
uwsgi --ini uwsgi.ini --lazy-apps --daemonize /var/log/arsenal.log
nginx -g "daemon off;"
