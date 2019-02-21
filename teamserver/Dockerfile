FROM nginx:alpine

EXPOSE 80

# Install package dependencies
RUN apk add --update python3 python3-dev gcc curl curl-dev make libc-dev libffi-dev linux-headers git

# Install pip dependencies
RUN mkdir -p /opt/arsenal/ && mkdir -p /opt/arsenal/flask_profile
COPY requirements /opt/arsenal/requirements
RUN pip3 install --upgrade pip
RUN pip3 install -r /opt/arsenal/requirements/prod.txt

# Configure nginx
COPY docker/teamserver/nginx.conf /etc/nginx/nginx.conf

# Configure the teamserver
COPY teamserver /opt/arsenal/teamserver
COPY bin /opt/arsenal/bin
COPY run.py /opt/arsenal/run.py
COPY docker/teamserver/uwsgi.ini /opt/arsenal/uwsgi.ini
COPY docker/teamserver/slack_api /opt/arsenal/teamserver/.slack_api

# Configure ENTRYPOINT
COPY docker/teamserver/entrypoint.sh /opt/arsenal/entrypoint.sh
RUN chmod 0755 /opt/arsenal/entrypoint.sh
ENTRYPOINT ["/opt/arsenal/entrypoint.sh"]
