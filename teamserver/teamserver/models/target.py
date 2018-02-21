"""
    This module defines a python object model for the Target document
    in the backend MongoDB database.
"""

from mongoengine import Document, DynamicEmbeddedDocument
from mongoengine.fields import StringField, DictField, ListField
from mongoengine.fields import EmbeddedDocumentListField

from .session import Session

from ..config import MAX_STR_LEN, MAX_BIGSTR_LEN
from ..config import COLLECTION_TARGETS
from ..config import SESSION_STATUSES

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
            {
                'fields': ['group_names']
            }
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
    credentials = EmbeddedDocumentListField(Credential)

    @property
    def sessions(self):
        """
        This property returns all session objects that are
        associated with this target.
        """
        return Session.objects(target_name=self.name) #pylint: disable=no-member

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
