"""
    This module defines a python object model for the Target document
    in the backend MongoDB database.
"""

from mongoengine import Document, DynamicEmbeddedDocument
from mongoengine.fields import StringField, DictField, ListField
from mongoengine.fields import EmbeddedDocumentListField
from mongoengine.errors import DoesNotExist

from .session import Session

from ..exceptions import CannotRenameTarget

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
                'fields': ['mac_addrs'],
                'unique': True
            }
        ]
    }

    name = StringField(
        required=True,
        null=False,
        max_length=MAX_STR_LEN,
        unique=True)

    mac_addrs = ListField(
        StringField(required=True, null=False, max_length=20),
        required=True,
        null=False,
        unique=True)

    facts = DictField(null=False)

    credentials = EmbeddedDocumentListField(Credential)

    _session_cache = None

    @staticmethod
    def get_by_name(name):
        """
        This method queries for the target object matching the name provided.
        """
        return Target.objects.get(name=name) #pylint: disable=no-member

    @staticmethod
    def get_by_macs(mac_addrs):
        """
        This method queries for the target object matching the mac_addrs provided.
        """
        return Target.objects.get(mac_addrs=mac_addrs) #pylint: disable=no-member

    @staticmethod
    def list():
        """
        This method queries for all target objects.
        """
        return Target.objects() #pylint: disable=no-member

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
            include_facts=False,
            include_sessions=False,
            include_credentials=False):
        """
        This property returns a filtered JSON document representation of the target.
        """
        doc = {
            'name': self.name,
            'status': self.status,
            'lastseen': self.lastseen,
            'mac_addrs': self.mac_addrs,
        }
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

    def rename(self, new_name):
        """
        This method renames the target.
        """
        try:
            Target.get_by_name(new_name)
            raise CannotRenameTarget('Target with new_name already exists.')
        except DoesNotExist:
            pass

        self.name = new_name
        self.save()
