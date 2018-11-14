# Arsenal [![Build Status](https://travis-ci.org/KCarretto/Arsenal.svg?branch=master)](https://travis-ci.org/KCarretto/Arsenal) ![python 3.6](https://img.shields.io/badge/python-3.6-green.svg)
Extensible Red Team Framework

## Overview
Arsenal is a framework designed to be a back-end for Red Team command and control operations. It allows many Agent-C2 models to be integrated into one system, with a great interface and many useful features. The goal is to limit the time Red Team spends on back-end development, and invest more resources into the malware that is distributed to target systems.  

### Feature Highlights
* Integrates with custom implants and C2 servers with ease
* Easily group target machines and interact with all of them at once
* 3rd Party applications can integrate using outgoing webhooks (i.e. Slack Integration)
* Register agents and prevent them from receiving unsupported commands
* Protected by authentication and custom RBAC implementation to restrict what users have access to
* Easy to use console with autocomplete, history searching, and more
* Enable action attribution, know who on your team did what and when

## Quick Start
Here are some quick deployment instructions to set up on Ubuntu 16.04 (The project will work across various distros however). It is recommended to loadbalance the teamserver for production use.

### Fast install
Note: Fix permissions (i.e. not require sudo) at your leisure
Optionally remove the new argument if you do not wish to populate the db with defaults.

```
sudo git clone https://github.com/kcarretto/arsenal /opt/arsenal
cd /opt/arsenal
sudo chmod +x install.sh
./install.sh new
```

### Install dependencies
`sudo apt-get update && sudo apt-get install docker.io git curl`

### Clone this repository
`sudo git clone https://github.com/kcarretto/arsenal /opt/arsenal`

### Install docker compose

`sudo curl -L https://github.com/docker/compose/releases/download/1.20.1/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose`

`sudo chmod +x /usr/local/bin/docker-compose`

### Deploy with docker compose
`mkdir -p /var/log/arsenal`

`cd /opt/arsenal; docker-compose up -d >> /var/log/arsenal/stdout.log 2>> /var/log/arsenal/stderr.log`

### Configure database defaults
`docker exec -it arsenal_teamserver_1 /bin/sh -c "cd /opt/arsenal/bin; python3 setup.py"`
This will populate the database with default users and roles defined in `bin/setup.py`

### Additional Information
The teamserver will now launch using docker-compose. To ensure that it is functioning properly, you may run `curl 127.0.0.1/status` and you should receive the teamserver's status back. You may also install the teamserver to the system without docker, please see `/contrib` for useful setup scripts, service files, and installation information.
