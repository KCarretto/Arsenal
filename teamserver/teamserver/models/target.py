"""
    This module defines a python object model for the Target document
    in the backend MongoDB database.
"""
import time

from mongoengine import Document, DynamicEmbeddedDocument, EmbeddedDocument
from mongoengine.fields import StringField, DictField, FloatField, ListField
from mongoengine.fields import EmbeddedDocumentListField

from ..config import MAX_STR_LEN, MAX_BIGSTR_LEN
from ..config import COLLECTION_TARGETS
from ..config import SESSION_CHECK_THRESHOLD, SESSION_CHECK_MODIFIER, SESSION_STATUSES


class Credential(DynamicEmbeddedDocument):
    """
    This class represents information that can be used to access a
    target, usually in the form of credentials. The below formatting
    is suggested, so that automated tasks can be executed, but it is
    a dynamic document, so data can be added here at will.
    """
    user = StringField(max_length=MAX_STR_LEN)
    password = StringField(max_length=MAX_STR_LEN)
    service = StringField(max_length=MAX_STR_LEN)
    key = StringField(max_length=MAX_BIGSTR_LEN)

class SessionHistory(Document):
    """
    This class stores historical information about a session, and
    will be searched for infrequently. It is updated when a session
    checks in.
    """
    checkin_timestamps = ListField(FloatField(required=True, null=False), required=True, null=False)

class Session(EmbeddedDocument):
    """
    This class represents a running instance of the agent on a
    target system. It is responsible for running actions created
    by the user.

    This class also has an associated class SessionHistory,
    which stores less frequently accessed data, that tends to grow
    rapidly over time.
    """
    history_id = StringField(required=True, null=False, max_length=MAX_STR_LEN)
    servers = ListField(
        StringField(required=True, null=False, max_length=MAX_STR_LEN),
        required=True,
        null=False)
    interval = FloatField(required=True, null=False)
    interval_delta = FloatField(required=True, null=False)
    config_dict = DictField(required=True, null=False)
    timestamp = FloatField(required=True, null=False)

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
        max_time = self.timestamp + self.interval + self.interval_delta + SESSION_CHECK_THRESHOLD

        if time.time() > max_time*SESSION_CHECK_MODIFIER:
            return SESSION_STATUSES.get('inactive', 'inactive')
        elif time.time() > max_time:
            return SESSION_STATUSES.get('missing', 'missing')

        return SESSION_STATUSES.get('active', 'active')

    @property
    def history(self):
        """
        Performs a query to retrieve history information about this session.
        """
        pass

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
                self.config_dict[key] = kwargs[key] #pylint: disable=unsupported-assignment-operation


class Target(Document):
    """
    This class represents a target system. It stores facts about the
    system, any sessions, as well as additional settings like groups.
    It's status is represented as the best status of all sessions
    associated with this target.
    """

    meta = {
        'collection': COLLECTION_TARGETS,
        'indexes': [
            {
                'fields': ['name'],
                'unique': True
            },
        ]
    }

    name = StringField(
        required=True,
        null=False,
        max_length=MAX_STR_LEN,
        unique=True,
        primary_key=True)
    facts = DictField(required=True, null=False)
    group_names = ListField(StringField(null=False, max_length=MAX_STR_LEN))
    sessions = EmbeddedDocumentListField(Session)

    @property
    def status(self):
        """
        This property returns the target status, which is calculated
        as the best of all it's session statuses.
        """
        best_status = SESSION_STATUSES.get('inactive', 'inactive')
        active = SESSION_STATUSES.get('active', 'active')
        missing = SESSION_STATUSES.get('missing', 'missing')

        for session in self.sessions: #pylint: disable=not-an-iterable
            if session.status == active:
                return active
            elif session.status == missing:
                best_status = missing

        return best_status

    @property
    def lastseen(self):
        """
        This property returns the last seen time of the target,
        which is calculated as the minimum of it's Session timestamps.
        """
        return min([session.timestamp for session in self.sessions]) #pylint: disable=not-an-iterable
