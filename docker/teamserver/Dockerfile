FROM nginx:alpine

# Install package dependencies
RUN apk add --update python3 python3-dev gcc make libc-dev linux-headers git

# Configure nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Clone the teamserver
RUN git clone https://github.com/kcarretto/arsenal /opt/arsenal

# Configure teamserver
COPY config.py /opt/arsenal/teamserver/teamserver/config.py

# Install requirements
RUN pip3 install --upgrade pip
RUN pip3 install -r /opt/arsenal/teamserver/teamserver/requirements/prod.txt

# Configure ENTRYPOINT
COPY entrypoint.sh /opt/arsenal/entrypoint.sh
RUN chmod 0755 /opt/arsenal/entrypoint.sh
ENTRYPOINT ["/opt/arsenal/entrypoint.sh"]
