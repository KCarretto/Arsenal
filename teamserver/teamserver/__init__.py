"""
    Imports
"""
import sys
import logging
from logging.config import dictConfig
from typing import Dict, Optional

from flask import Flask
from flask_mongoengine import MongoEngine
from mongoengine import connect, MongoEngineConnectionError

from .config import MODE, PROFILE_DIR
from .config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS
from .config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
from .integrations.integration import Integration

DB = MongoEngine()


def _configure_logging(config: Optional[Dict] = None) -> None:
    opts = {
        "version": 1,
        "formatters": {
            "default": {"format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"}
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
    if config:
        opts.update(config)
    dictConfig(opts)


def create_app(**config_overrides):
    """
    Creates a flask application with the desired configuration settings
    and connects it to the database.
    """
    app = Flask(__name__)

    # Initialize logging
    _configure_logging()

    # Initialize configuration
    app.config.from_object("teamserver.config")
    app.config["MODE"] = MODE

    app.config["MONGODB_SETTINGS"] = {"db": DB_NAME, "host": DB_HOST, "port": DB_PORT}
    if DB_USER and DB_PASS:
        app.config["MONGODB_SETTINGS"]["username"] = DB_USER
        app.config["MONGODB_SETTINGS"]["password"] = DB_PASS

    app.config["CELERY_BROKER_URL"] = CELERY_BROKER_URL
    app.config["CELERY_RESULT_BACKEND"] = CELERY_RESULT_BACKEND

    # Override configuration options
    app.config.update(config_overrides)

    # Initialize DEBUG
    if MODE.upper() == "DEBUG":
        # Enable debug logging
        app.logger.setLevel(logging.DEBUG)

        # Enable profiling
        from werkzeug.contrib.profiler import ProfilerMiddleware

        app.config["PROFILE"] = True
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[50], profile_dir=PROFILE_DIR)

        # Enable mongodb debug toolbar
        from flask_debugtoolbar import DebugToolbarExtension

        app.config["DEBUG_TB_PANELS"] = ["flask_mongoengine.panels.MongoDebugPanel"]
        app.debug_toolbar = DebugToolbarExtension(app)
    else:
        app.logger.setLevel(logging.WARNING)

    # Initialize the database
    try:
        DB.init_app(app)
    except MongoEngineConnectionError as conn_err:
        print(conn_err)
        sys.exit("Could not connect to database.")

    # Import endpoints
    from teamserver.router import API

    app.register_blueprint(API)

    app.logger.info(f"Initialized Arsenal Teamserver [{MODE}]")
    return app
