"""
    This module defines a python object model for the Action document
    in the backend MongoDB database.
"""
import time

from mongoengine import DynamicDocument, EmbeddedDocument
from mongoengine.fields import StringField, IntField, FloatField
from mongoengine.fields import BooleanField, EmbeddedDocumentField

from .session import Session

from ..config import MAX_STR_LEN, MAX_BIGSTR_LEN, ACTION_STATUSES, SESSION_STATUSES
from ..config import COLLECTION_ACTIONS, ACTION_STALE_THRESHOLD


class Response(EmbeddedDocument):
    """
    This class represents a response from an action.

        stdout: Any output the action genereated.
        stderr: Any error messages the action generated.
        start_time: The local system time that the action started.
        end_time: The local system time that the action completed.
        error: A boolean representing if the action encountered an error.
    """

    stdout = StringField(required=True, max_length=MAX_BIGSTR_LEN)
    stderr = StringField(required=True, max_length=MAX_BIGSTR_LEN)
    start_time = FloatField(required=True, null=False)
    end_time = FloatField(required=True, null=False)
    error = BooleanField(default=True)

class Action(DynamicDocument):
    """
    This class represents an action, which is assigned to a target
    and then sent to a session. It's status is based on the status of
    the session it was sent to, as well as if the session has sent or
    responded to the action yet.
    """
    meta = {
        'collection': COLLECTION_ACTIONS,
        'indexes': [
            {
                'fields': ['action_id'],
                'unique': True
            },
            {
                'fields': ['target_name']
            },
            {
                'fields': ['session_id']
            },
        ]
    }
    action_id = StringField(required=True, null=False, max_length=MAX_STR_LEN)
    action_string = StringField(required=True, null=False, max_length=MAX_BIGSTR_LEN)
    action_type = IntField(required=True, null=False)
    target_name = StringField(required=True, null=False, max_length=MAX_STR_LEN)
    session_id = StringField(max_length=MAX_STR_LEN)
    bound_session_id = StringField(max_length=MAX_STR_LEN)

    queue_time = FloatField(required=True, null=False)
    sent_time = FloatField()
    complete_time = FloatField()

    response = EmbeddedDocumentField(Response)

    @staticmethod
    def get_by_id(action_id):
        """
        This method queries for the action object matching the id provided.
        """
        return Action.objects.get(action_id=action_id) #pylint: disable=no-member

    @property
    def session(self):
        """
        This property queries for the associated session object.
        """
        return Session.objects.get(session_id=self.session_id) #pylint: disable=no-member

    @property
    def status(self): #pylint: disable=too-many-return-statements
        """
        This property returns the current status of the action based
        on the status of it's assigned session, as well as if it has
        been retrieved or contains a response.
        """
        # Return queued if no session has been assigned
        if self.session_id is None:
            if time.time() > self.queue_time + ACTION_STALE_THRESHOLD:
                return ACTION_STATUSES.get('stale', 'stale')
            return ACTION_STATUSES.get('queued', 'queued')
        # Return complete if we have received a response
        elif self.response is not None:
            if self.response.error:
                return ACTION_STATUSES.get('error', 'error')
            return ACTION_STATUSES.get('complete', 'complete')

        # TODO: Raise an error if the session does not exist

        session_status = self.session.status

        if session_status == SESSION_STATUSES.get('active', 'active'):
            return ACTION_STATUSES.get('sent', 'sent')

        if session_status == SESSION_STATUSES.get('missing', 'missing'):
            return ACTION_STATUSES.get('failing', 'failing')

        return ACTION_STATUSES.get('failed', 'failed')

    def assign_to(self, session):
        """
        This function assigns this action to a session. It will update
        the current action object.
        """
        # TODO: Generate Event

        if self.bound_session_id is not None and session.session_id != self.bound_session_id:
            # TODO: Raise error for assigning to non-bound session
            pass

        self.session_id = session.session_id
        self.sent_time = time.time()
        self.save()

    def assign_to_id(self, session_id):
        """
        This function will assign the action to the given session_id.
        It does not attempt to lookup the session.
        """
        # TODO: Generate Event

        if self.bound_session_id is not None and session_id != self.bound_session_id:
            # TODO: Raise error for assigning to non-bound session
            pass

        self.session_id = session_id
        self.sent_time = time.time()
        self.save()

    def submit_response(self, response):
        """
        This function will update the action object with a response object,
        and set appropriate timestamps.
        """
        # TODO: Generate Event
        self.response = response
        self.complete_time = time.time()
        self.save()
