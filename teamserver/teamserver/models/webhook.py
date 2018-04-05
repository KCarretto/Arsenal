"""
    This module defines a python object model for a webhook.

    Each webhook is owned by a particular user, and can only be managed
    by that user.

    A webhook is used when an event is triggered,
    the event's data will be posted to the given post_url.
"""
from mongoengine import Document
from mongoengine.fields import StringField

from ..config import COLLECTION_WEBHOOKS, MAX_STR_LEN

class Webhook(Document):
    """
    This class represents a Webhook.
    """
    meta = {
        'collection': COLLECTION_WEBHOOKS,
        'indexes': [
            {
                'fields': ['key'],
                'unique': True
            }
        ]
    }
    owner = StringField(required=True, null=False, max_length=MAX_STR_LEN)
    post_url = StringField(required=True, null=False, max_length=MAX_STR_LEN)
    event_trigger = StringField(required=True, null=False, max_length=MAX_STR_LEN)

    @property
    def document(self):
        """
        Returns a document for this object.
        """
        return {
            'owner': self.owner,
            'post_url': self.post_url,
            'trigger': self.event_trigger,
        }

    def remove(self):
        """
        Remove this document from the database, and perform any related cleanup.
        """
        self.delete()

