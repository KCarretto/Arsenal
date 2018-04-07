"""
This module contains logging functionality for the teamserver.
"""
import time

from ..config import LOG_LEVEL, LOG_LEVELS, APPLICATION
from ..models import Log

def log(level, message, application=APPLICATION):
    """
    Log a message for the application at the given level.
    """
    if LOG_LEVELS.get(level.upper(), 0) >= LOG_LEVELS.get(LOG_LEVEL, 0):
        entry = Log(
            timestamp=time.time(),
            application=application,
            level=level.upper(),
            message=message
        )
        entry.save(force_insert=True)
