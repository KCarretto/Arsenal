#!/bin/sh

cd /opt/arsenal/
mkdir -p /var/log/arsenal
celery multi start 5 --app=teamserver.events -f /var/log/arsenal/celery.log
uwsgi --ini uwsgi.ini --lazy-apps --daemonize /var/log/arsenal/uwsgi.log
nginx -g "daemon off;"
