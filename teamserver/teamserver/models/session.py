"""
This module defines the Session object.
"""
from mongoengine import DynamicEmbeddedDocument, EmbeddedDocumentField
from mongoengine import StringField, FloatField, IntField, BooleanField, ListField

from ..config import COLLECTION_SESSIONS
from .model import Model

class SessionConfig(DynamicEmbeddedDocument):
    """
    This object models the configuration information for a given session.
    """
    interval = IntField(min_value=0, required=True, null=False)
    delta = IntField(min_value=0, required=True, null=False)
    servers = ListField(
        StringField(
            regex='.*://.*',    # Force explicit protocol definition
            required=True,
            null=False
        ),
        required=True,
        null=False
    )

class Session(Model):
    """
    This object models a running instance of the agent on a target system. It is responsible for
    running actions created by the user. This class also has an associated class SessionHistory,
    which stores less frequently accessed data, that tends to grow rapidly over time.
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
            },
            {
                'fields': ['agent_version']
            }
        ]
    }

    session_id = StringField(required=True, unique=True, null=False)
    target_name = StringField(required=True, null=False)
    timestamp = FloatField(required=True, null=False)
    agent_version = StringField(required=False, default='unknown')
    config = EmbeddedDocumentField(SessionConfig, required=True, null=False)

    archived = BooleanField(required=False, null=False, default=False)
