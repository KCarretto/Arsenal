"""
    This module defines a python object model for the Log document
    in the backend MongoDB database.
"""
import time

from mongoengine import Document
from mongoengine.fields import BooleanField, StringField, FloatField

from ..config import MAX_STR_LEN, MAX_BIGSTR_LEN, COLLECTION_LOGS
from ..config import LOG_LEVELS, LOG_LEVEL, APPLICATION

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

class Log(Document):
    """
    This class represents a log message. It could be from any application
    that has access to the teamserver API and the proper permissions. It
    might also be from the internal teamserver, a C2, or an agent.
    """
    meta = {
        'collection': COLLECTION_LOGS,
        'indexes': [
            {
                'fields': ['application'],
            }
        ]
    }
    timestamp = FloatField(required=True, null=False)
    application = StringField(required=True, null=False, max_length=MAX_STR_LEN)
    level = StringField(required=True, null=False, choices=LOG_LEVELS.keys())
    message = StringField(required=True, null=False, max_length=MAX_BIGSTR_LEN)
    archived = BooleanField(default=False)

    @staticmethod
    def list_logs(include_archived=False, application=None, since=0):
        """
        Return a list of logs.
        Optionally include archived logs.
        Optionally filter by application.
        Optionally filter by a timestamp
        """
        if application is not None:
            if include_archived:
                return Log.objects(application=application, timestamp__gte=since) # pylint: disable=no-member
            return Log.objects(application=application, archived=False, timestamp__gte=since) # pylint: disable=no-member
        elif include_archived:
            return Log.objects(timestamp__gte=since) # pylint: disable=no-member
        return Log.objects(archived=False, timestamp__gte=since) # pylint: disable=no-member

    @property
    def document(self):
        """
        This property filters and returns the JSON information for a queried group.
        """
        return {
            'timestamp': self.timestamp,
            'application': self.application,
            'level': self.level,
            'message': self.message,
        }
