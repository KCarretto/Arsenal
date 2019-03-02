"""
    This module defines a python object model for the Target document
    in the backend MongoDB database.
"""

import time

from mongoengine import Document
from mongoengine.fields import StringField, DictField, ListField, BooleanField

from .session import Session

from ..config import MAX_STR_LEN, MAX_BIGSTR_LEN
from ..config import COLLECTION_TARGETS, COLLECTION_TARGET_CREDS
from ..config import SESSION_STATUSES, SESSION_ARCHIVE_MODIFIER


class Credential(Document):
    """
    This class represents a set of credentials for the target system.
    """

    meta = {"collection": COLLECTION_TARGET_CREDS, "indexes": [{"fields": ["target_name"]}]}
    target_name = StringField(max_length=MAX_STR_LEN)
    user = StringField(max_length=MAX_STR_LEN)
    key = StringField(max_length=MAX_BIGSTR_LEN)
    service = StringField(max_length=MAX_STR_LEN)
    valid = BooleanField(null=False, default=True)

    @property
    def document(self):
        """
        Return as formatted JSON.
        """
        return {
            "target_name": self.target_name,
            "user": self.user,
            "key": self.key,
            "service": self.service,
            "valid": self.valid,
        }


class Target(Document):
    """
    This class represents a target system. It stores facts about the
    system, any sessions, as well as additional settings like groups.
    It's status is represented as the best status of all sessions
    associated with this target.
    """

    meta = {
        "collection": COLLECTION_TARGETS,
        "indexes": [{"fields": ["name"], "unique": True}, {"fields": ["uuid"], "unique": True}],
    }

    name = StringField(required=True, null=False, max_length=MAX_STR_LEN, unique=True)

    uuid = StringField(required=True, null=False, max_length=MAX_BIGSTR_LEN, unique=True)

    public_ips = ListField(
        StringField(required=True, null=False, max_length=MAX_STR_LEN), required=False
    )

    facts = DictField(null=False)

    _session_cache = None

    @staticmethod
    def get_by_name(name):
        """
        This method queries for the target object matching the name provided.
        """
        return Target.objects.get(name__iexact=name)  # pylint: disable=no-member

    @staticmethod
    def get_by_uuid(uuid):
        """
        This method queries for the target object matching the mac_addrs provided.
        """
        return Target.objects.get(uuid__iexact=uuid)  # pylint: disable=no-member

    @staticmethod
    def list_targets(params):
        """
        This method queries for all target objects.
        """
        # Attempt to limit the data retrieved
        fields = ["name", "uuid", "public_ips"]
        if params.get("include_facts", False):
            fields += ["facts"]

        return Target.objects().only(*fields)  # pylint: disable=no-member

    @property
    def sessions(self):
        """
        This property returns all session objects that are
        associated with this target. Archive any sessions that have
        not been seen in a long period of time.
        """
        sessions = list(
            Session.objects(target_name=self.name, archived=False)  # pylint: disable=no-member
        )
        for session in sessions:
            threshold = session.timestamp + (session.interval + session.interval_delta)
            threshold *= SESSION_ARCHIVE_MODIFIER
            if time.time() > threshold:
                session.archive()
                sessions.remove(session)

        self._session_cache = sessions
        return sessions

    @property
    def credentials(self):
        """
        This property returns all valid credentials for a target.
        """
        return list(
            Credential.objects(valid=True, target_name=self.name)  # pylint: disable=no-member
        )

    @property
    def status(self):
        """
        This property returns the target status, which is calculated
        as the best of all it's session statuses.
        """
        best_status = SESSION_STATUSES.get("inactive", "inactive")
        active = SESSION_STATUSES.get("active", "active")
        missing = SESSION_STATUSES.get("missing", "missing")

        for session in self.sessions:  # pylint: disable=not-an-iterable
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
            return min(
                [session.timestamp for session in sessions]
            )  # pylint: disable=not-an-iterable
        return -1

    def document(self, include_status=True, include_facts=False, include_sessions=False):
        """
        This property returns a filtered JSON document representation of the target.
        """
        doc = {"name": self.name, "uuid": self.uuid, "public_ips": self.public_ips}
        if include_status:
            doc["status"] = self.status
            doc["lastseen"] = self.lastseen
        if include_facts:
            doc["facts"] = self.facts
        if include_sessions:
            sessions = self._session_cache if self._session_cache else self.sessions
            doc["sessions"] = [session.document for session in sessions]

        return doc

    def set_facts(self, facts):
        """
        This method sets the facts dictionary for a target.
        """
        for key, value in facts.items():
            self.facts[key] = value  # pylint: disable=unsupported-assignment-operation
        self.save()

    def add_public_ip(self, public_ip):
        """
        Associate a public ip with the target.
        """
        if public_ip not in self.public_ips:  # pylint: disable=unsupported-membership-test
            self.public_ips.append(public_ip)  # pylint: disable=no-member
            self.save()

    def remove(self):
        """
        Remove this document from the database, and perform any related cleanup.
        """
        self.delete()
