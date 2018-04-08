FROM nginx:ubuntu

# Update
RUN apt-get update

# Configure nginx
COPY nginx.conf /etc/nginx/nginx.conf
RUN mkdir -p /etc/nginx/certs
COPY arsenal.cert /etc/nginx/certs/arsenal.cert
COPY arsenal.key /etc/nginx/certs/arsenal.key

# Copy teamserver
COPY ../teamserver /opt/arsenal

# Configure teamserver
COPY config.py /opt/arsenal/teamserver/config.py
