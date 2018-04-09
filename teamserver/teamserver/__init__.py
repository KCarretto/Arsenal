"""
    Imports
"""
import sys

from flask import Flask

from flask_mongoengine import MongoEngine
from mongoengine import connect, MongoEngineConnectionError

from .config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS
from .config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

DB = MongoEngine()

def create_app(**config_overrides):
    """
    Creates a flask application with the desired configuration settings
    and connects it to the database.
    """
    app = Flask(__name__)

    # Initialize configuration
    app.config.from_object('teamserver.config')
    app.config['MONGODB_SETTINGS'] = {
        'db': DB_NAME,
        'host': DB_HOST,
        'port': DB_PORT
    }
    if DB_USER and DB_PASS:
        app.config['MONGODB_SETTINGS']['username'] = DB_USER
        app.config['MONGODB_SETTINGS']['password'] = DB_PASS

    app.config['CELERY_BROKER_URL'] = CELERY_BROKER_URL
    app.config['CELERY_RESULT_BACKEND'] = CELERY_RESULT_BACKEND

    # Override configuration options
    app.config.update(config_overrides)

    # Initialize the database
    try:
        DB.init_app(app)
    except MongoEngineConnectionError as conn_err:
        print(conn_err)
        sys.exit('Could not connect to database.')

    # Import endpoints
    from teamserver.router import API
    app.register_blueprint(API)


    return app
