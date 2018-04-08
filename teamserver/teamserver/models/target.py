"""
    This module defines a python object model for the Target document
    in the backend MongoDB database.
"""

import time

from mongoengine import Document, DynamicEmbeddedDocument
from mongoengine.fields import StringField, DictField
from mongoengine.fields import EmbeddedDocumentListField

from .session import Session

from ..config import MAX_STR_LEN, MAX_BIGSTR_LEN
from ..config import COLLECTION_TARGETS
from ..config import SESSION_STATUSES, SESSION_ARCHIVE_MODIFIER

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
                'fields': ['uuid'],
                'unique': True
            }
        ]
    }

    name = StringField(
        required=True,
        null=False,
        max_length=MAX_STR_LEN,
        unique=True)

    #mac_addrs = ListField(
    #    StringField(required=True, null=False, max_length=20),
    #    required=True,
    #    null=False,
    #    unique=True)

    uuid = StringField(required=True, null=False, max_length=MAX_BIGSTR_LEN, unique=True)

    facts = DictField(null=False)

    credentials = EmbeddedDocumentListField(Credential)

    _session_cache = None

    @staticmethod
    def get_by_name(name):
        """
        This method queries for the target object matching the name provided.
        """
        return Target.objects.get(name__iexact=name) #pylint: disable=no-member

    @staticmethod
    def get_by_uuid(uuid):
        """
        This method queries for the target object matching the mac_addrs provided.
        """
        return Target.objects.get(uuid__iexact=uuid) #pylint: disable=no-member

    @staticmethod
    def list_targets():
        """
        This method queries for all target objects.
        """
        return Target.objects() #pylint: disable=no-member

    @property
    def sessions(self):
        """
        This property returns all session objects that are
        associated with this target. Archive any sessions that have
        not been seen in a long period of time.
        """
        sessions = Session.objects(target_name=self.name, archived=False) #pylint: disable=no-member
        for session in sessions:
            threshold = session.timestamp + (session.interval + session.interval_delta)
            threshold *= SESSION_ARCHIVE_MODIFIER
            if time.time() > threshold:
                session.archive()
                sessions.remove(session)
        return sessions

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
        This function returns the last seen time of the target,
        which is calculated as the minimum of it's Session timestamps.

        This function will return -1 if the target has never been seen.
        """
        sessions = self.sessions
        if sessions:
            return min([session.timestamp for session in sessions]) #pylint: disable=not-an-iterable
        return -1

    def document(
            self,
            include_status=True,
            include_facts=False,
            include_sessions=False,
            include_credentials=False):
        """
        This property returns a filtered JSON document representation of the target.
        """
        doc = {
            'name': self.name,
            'uuid': self.uuid,
        }
        if include_status:
            doc['status'] = self.status
            doc['lastseen'] = self.lastseen
        if include_facts:
            doc['facts'] = self.facts
        if include_sessions:
            doc['sessions'] = self.sessions
        if include_credentials:
            doc['credentials'] = self.credentials

        return doc

    def set_facts(self, facts):
        """
        This method sets the facts dictionary for a target.
        """
        for key, value in facts.items():
            self.facts[key] = value #pylint: disable=unsupported-assignment-operation
        self.save()

    def remove(self):
        """
        Remove this document from the database, and perform any related cleanup.
        """
        self.delete()
