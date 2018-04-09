FROM nginx:alpine

# Install package dependencies
RUN apk add --update python3 python3-dev gcc make libc-dev libffi-dev linux-headers git

# Configure nginx
COPY docker/teamserver/nginx.conf /etc/nginx/nginx.conf

# Copy the teamserver
RUN mkdir -p /opt/arsenal
COPY teamserver /opt/arsenal/teamserver
COPY requirements /opt/arsenal/requirements
COPY run.py /opt/arsenal/run.py

# Configure teamserver
COPY docker/teamserver/uwsgi.ini /opt/arsenal/teamserver/uwsgi.ini
COPY docker/teamserver/config.py /opt/arsenal/teamserver/teamserver/config.py

# Install requirements
RUN pip3 install --upgrade pip
RUN pip3 install -r /opt/arsenal/teamserver/requirements/prod.txt

# Configure ENTRYPOINT
COPY docker/teamserver/entrypoint.sh /opt/arsenal/entrypoint.sh
RUN chmod 0755 /opt/arsenal/entrypoint.sh
ENTRYPOINT ["/opt/arsenal/entrypoint.sh"]
