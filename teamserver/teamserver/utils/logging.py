"""
This module contains logging functionality for the teamserver.
"""
import time
from flask import current_app

import teamserver.events.worker as events

from ..config import LOG_LEVEL, LOG_LEVELS, APPLICATION
from ..models import Log

def log(level, message, application=APPLICATION):
    """
    Log a message for the application at the given level.
    """
    message_level = LOG_LEVELS.get(level.upper(), 0)
    current_level = LOG_LEVELS.get(LOG_LEVEL, 0)
    if  message_level >= current_level:
        entry = Log(
            timestamp=time.time(),
            application=application,
            level=level.upper(),
            message=message
        )
        entry.save(force_insert=True)

        if message_level >= LOG_LEVELS.get('CRIT', 3):
            if not current_app.config.get('DISABLE_EVENTS', False):
                events.trigger_event.delay(
                    event='logged_error',
                    log=entry.document
                )

