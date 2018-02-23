"""
    This module defines a python object model for the Target document
    in the backend MongoDB database.
"""
import time

from mongoengine import Document
from mongoengine.fields import StringField, DictField, FloatField, ListField

from ..config import MAX_STR_LEN
from ..config import COLLECTION_SESSIONS, COLLECTION_SESSION_HISTORIES
from ..config import SESSION_CHECK_THRESHOLD, SESSION_CHECK_MODIFIER, SESSION_STATUSES

class SessionHistory(Document):
    """
    This class stores historical information about a session, and
    will be searched for infrequently. It is updated when a session
    checks in.
    """
    meta = {
        'collection': COLLECTION_SESSION_HISTORIES,
        'indexes': [
            {
                'fields': ['session_id'],
                'unique': True
            }
        ]
    }
    session_id = StringField(required=True, null=False, max_length=MAX_STR_LEN)
    checkin_timestamps = ListField(FloatField(required=True, null=False), required=True, null=False)

    def add_checkin(self, timestamp):
        """
        This function adds a checkin timestamp to a list
        of session checkin timestamps.
        """
        self.checkin_timestamps.append(timestamp) #pylint: disable=no-member


class Session(Document):
    """
    This class represents a running instance of the agent on a
    target system. It is responsible for running actions created
    by the user.

    This class also has an associated class SessionHistory,
    which stores less frequently accessed data, that tends to grow
    rapidly over time.
    """
    meta = {
        'collection': COLLECTION_SESSIONS,
        'indexes': [
            {
                'fields': ['session_id'],
                'unique': True
            },
            {
                'fields': ['target_name']
            }
        ]
    }
    session_id = StringField(required=True, null=False, max_length=MAX_STR_LEN)
    target_name = StringField(required=True, null=False, max_length=MAX_STR_LEN)
    timestamp = FloatField(required=True, null=False)

    servers = ListField(
        StringField(required=True, null=False, max_length=MAX_STR_LEN),
        required=True,
        null=False)
    interval = FloatField(required=True, null=False)
    interval_delta = FloatField(required=True, null=False)
    config_dict = DictField(null=False)

    @staticmethod
    def get_by_id(session_id):
        """
        This method queries for the session object matching the name provided.
        """
        return Session.objects.get(session_id=session_id) #pylint: disable=no-member

    @property
    def config(self):
        """
        This property returns the session configuration,
        overriding all reserved keys with their proper values.

        config_dict should never be used directly.
        """
        self.config_dict['interval'] = self.interval #pylint: disable=unsupported-assignment-operation
        self.config_dict['interval_delta'] = self.interval_delta #pylint: disable=unsupported-assignment-operation
        self.config_dict['servers'] = self.servers #pylint: disable=unsupported-assignment-operation

        return self.config_dict

    @property
    def status(self):
        """
        This property returns the session status,
        which is based on the current interval setting
        and the last seen timestamp.
        """
        max_time = self.interval + self.interval_delta + SESSION_CHECK_THRESHOLD

        if time.time() > self.timestamp+(max_time*SESSION_CHECK_MODIFIER):
            return SESSION_STATUSES.get('inactive', 'inactive')
        elif time.time() > self.timestamp+max_time:
            return SESSION_STATUSES.get('missing', 'missing')

        return SESSION_STATUSES.get('active', 'active')

    @property
    def history(self):
        """
        Performs a query to retrieve history information about this session.
        """
        return SessionHistory.objects.get(session_id=self.session_id) #pylint: disable=no-member

    def update_config(self, **kwargs):
        """
        This function will update a sessions config according to
        keywords. It will also validate types of reserved keywords.
        """
        for key, value in kwargs.items():
            # Check for reserved keys first, then set other options
            if key == 'interval' or key == 'interval_delta':
                if isinstance(value, float) and isinstance(value, int):
                    # TODO: Raise type exception
                    pass
                self.__setattr__(key, value)
            elif key == 'servers':
                if isinstance(value, list):
                    # TODO: Raise type exception
                    pass
                self.servers = value
            else:
                self.config_dict[key] = value #pylint: disable=unsupported-assignment-operation
