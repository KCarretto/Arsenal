"""
    This module defines a python object model for a webhook.

    Each webhook is owned by a particular user, and can only be managed
    by that user.

    A webhook is used when an event is triggered,
    the event's data will be posted to the given post_url.
"""
from mongoengine import Document
from mongoengine.fields import StringField, ListField

from ..config import COLLECTION_WEBHOOKS, MAX_STR_LEN

class Webhook(Document):
    """
    This class represents a Webhook.
    """
    meta = {
        'collection': COLLECTION_WEBHOOKS,
        'indexes': [
            {
                'fields': ['hook_id'],
                'unique': True
            }
        ]
    }

    hook_id = StringField(required=True, null=False, max_length=MAX_STR_LEN, unique=True)
    owner = StringField(required=True, null=False, max_length=MAX_STR_LEN)
    post_url = StringField(required=True, null=False, max_length=MAX_STR_LEN)
    event_triggers = ListField(
        StringField(required=True, null=False, max_length=MAX_STR_LEN),
        required=True,
        null=False)

    @staticmethod
    def get_subscribers(event):
        """
        Return a list of webhooks subscribed to a given event_trigger.
        """
        return Webhook.objects(event_triggers=event) # pylint: disable=no-member

    @staticmethod
    def get_hook(hook_id):
        """
        Return a webhook based on the given id.
        """
        return Webhook.objects.get(hook_id=hook_id) # pylint: disable=no-member

    @staticmethod
    def list_hooks(username):
        """
        Return a list of hooks owned by a given of a user.
        """
        return Webhook.objects(owner=username) # pylint: disable=no-member

    @property
    def document(self):
        """
        Returns a document for this object.
        """
        return {
            'owner': self.owner,
            'post_url': self.post_url,
            'triggers': self.event_triggers,
        }

    def remove(self):
        """
        Remove this document from the database, and perform any related cleanup.
        """
        self.delete()

