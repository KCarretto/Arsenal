cd /opt/arsenal/teamserver
uwsgi --ini uwsgi.ini --lazy-apps --daemonize /var/log/arsenal.log
nginx -g "daemon off;"
