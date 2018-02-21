"""
    Imports
"""
import sys

from flask import Flask
from flask_mongoengine import MongoEngine

from mongoengine import connect, MongoEngineConnectionError

db = MongoEngine()

def create_app(**config_overrides):
    """
    Creates a flask application with the desired configuration settings
    and connects it to the database.
    """
    app = Flask(__name__)
    app.config.from_object('teamserver.config')
    app.config['MONGODB_SETTINGS'] = {'db': 'arsenal_default'}
    from teamserver.router import endpoints
    app.register_blueprint(endpoints)
    app.config.update(config_overrides)
    try:
        db.init_app(app)
    except MongoEngineConnectionError as e:
        # TODO: Add logging
        print(e)
        sys.exit('Could not connect to database.')

    return app

