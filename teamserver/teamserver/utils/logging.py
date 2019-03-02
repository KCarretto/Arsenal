"""
This module contains logging functionality for the teamserver.
"""
import time
from flask import current_app

from ..config import LOG_LEVEL, LOG_LEVELS, APPLICATION
from ..models import Log


def log(level, message, application=APPLICATION):
    """
    Log a message for the application at the given level.
    """
    message_level = LOG_LEVELS.get(level.upper(), 0)
    if message_level >= LOG_LEVELS.get("CRIT", 3):
        current_app.logger.error(f"{application}: {message}")
    elif level.upper() == "DEBUG":
        current_app.logger.debug(f"{application}: {message}")
    else:
        current_app.logger.info(f"{application}: {message}")
