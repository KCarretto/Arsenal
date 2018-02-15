
"""
    Imports
"""
import sys

from flask import Flask
from flask_mongoengine import MongoEngine

from mongoengine import connect, MongoEngineConnectionError

from .config import DB_NAME, DB_HOST, DB_PORT, DB_USER, DB_PASS

"""
    Start App
"""
teamapp = Flask(__name__)

"""
    Connect to Database
"""
try:
    teamapp.config['MONGODB_SETTINGS'] = {'DB': DB_NAME, 'HOST': DB_HOST, 'PORT': DB_PORT}
    db = MongoEngine(teamapp)
    # TODO: Support Database authentication
except MongoEngineConnectionError as e:
    # TODO: Add logging
    sys.exit("Could not connect to database.")

"""
    Register Endpoints
"""
from . import router

