#!/bin/bash

# Quick installation for Arsenal teamserver
# Compatible with Ubuntu 16.04
#
# You may need to run this script as root, or configure proper user permissions
#
# usage: ./install.sh new
#   Install a new teamserver, and setup the database with defaults
#
# usage: ./install.sh
#   Install a new teamserver, but don't populate the database
echo "Installing dependencies" | tee install.log
apt-get update -y && apt-get install docker.io git curl > install.log && echo "Installed packages" | tee install.log
curl -L https://github.com/docker/compose/releases/download/1.20.1/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose >> install.log && echo "Installed docker-compose" | tee install.log
sudo chmod +x /usr/local/bin/docker-compose >> install.log && echo "docker-compose marked executable" | tee install.log
echo "Dependencies installed" | tee install.log
echo -e "\nConfiguring logging" | tee install.log
mkdir -p /var/log/arsenal >> install.log && echo "Created log directory '/var/log/arsenal'" | tee install.log
echo -e "\nSpinning up teamserver with defaults" | tee install.log
docker-compose up -d >> /var/log/arsenal/stdout.log 2>> /var/log/arsenal/stderr.log
echo "Installation STDOUT:" | tee install.log
echo "$(cat /var/log/arsenal/stdout.log)" | tee install.log
echo "Installation STDERR:" | tee install.log
echo "$(cat /var/log/arsenal/stderr.log)" | tee install.log

if [ "$1" = "new" ]; then
  echo "Configuring initial db using bin/setup.py" | tee install.log
  echo -e "\n\nSaving these credentials to 'init.creds'" | tee install.log
  docker exec -it arsenal_teamserver_1 /bin/sh -c "cd /opt/arsenal/bin; python3 setup.py" | tee init.creds
  echo "DB Setup complete"
fi

echo -e "\nMoving log to /var/log/arsenal/install.log" | tee install.log
mv install.log /var/log/arsenal/install.log

echo -e "\nInstallation complete"
