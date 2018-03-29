"""
    This module defines a python object model for the GroupAction document
    in the backend MongoDB database.
"""
from mongoengine import Document
from mongoengine.fields import StringField, ListField, BooleanField

from .action import Action

from ..config import COLLECTION_GROUP_ACTIONS, MAX_STR_LEN, ACTION_STATUSES, GROUP_ACTION_STATUSES

class GroupAction(Document):
    """
    This class represents a group action, which is created to track actions
    across multiple targets. This document primarily serves as a reference,
    pointing to all the action documents themselves.
    """
    meta = {
        'collection': COLLECTION_GROUP_ACTIONS,
        'indexes': [
            {
                'fields': ['group_action_id'],
                'unique': True
            },
        ]
    }
    group_action_id = StringField(required=True, null=False, max_length=MAX_STR_LEN)
    action_string = StringField(required=True, null=False, max_length=MAX_STR_LEN)
    action_ids = ListField(
        StringField(required=True, null=False, max_length=MAX_STR_LEN), required=True, null=False)
    cancelled = BooleanField(default=False)

    @staticmethod
    def list_group_actions():
        """
        This method queries for all group action objects.
        """
        return GroupAction.objects() #pylint: disable=no-member

    @staticmethod
    def get_by_id(group_action_id):
        """
        This method queries for the group action object matching the id provided.
        """
        return GroupAction.objects.get(group_action_id=group_action_id) #pylint: disable=no-member

    @property
    def actions(self):
        """
        This property returns all of a group_actions associated action objects.
        """
        return [Action.get_by_id(action_id) for action_id in self.action_ids] #pylint: disable=not-an-iterable


    @property
    def document(self): #TODO: Add filter options
        """
        This property returns a document describing statuses for all of it's included actions.
        """
        actions = self.actions

        return {
            'group_action_id': self.group_action_id,
            'action_string': self.action_string,
            'status': self.get_status(actions),
            'action_ids': self.action_ids,
            'actions': [action.document for action in actions]
        }

    def get_status(self, actions=None):
        """
        This property determines the status of the group action, based on all of
        it's included actions. If no included action list is passed to this function,
        it will resolve them.
        """
        if self.cancelled:
            return GROUP_ACTION_STATUSES.get('cancelled', 'cancelled')
        if actions is None:
            actions = self.actions

        queued = 0
        sent = 0
        complete = 0

        for action in actions:
            status = action.status
            if status == ACTION_STATUSES.get('queued', 'queued'):
                queued += 1
            if status == ACTION_STATUSES.get('sent', 'sent'):
                sent += 1
            if status == ACTION_STATUSES.get('complete', 'complete'):
                complete += 1

        if complete == len(actions):
            return GROUP_ACTION_STATUSES.get('success', 'success')

        if sent > 0:
            return GROUP_ACTION_STATUSES.get('in progress', 'in progress')

        if queued > 0:
            return GROUP_ACTION_STATUSES.get('queued', 'queued')

        if complete > 0:
            return GROUP_ACTION_STATUSES.get('mixed success', 'mixed success')

        return GROUP_ACTION_STATUSES.get('failed', 'failed')

    def cancel(self):
        """
        Cancel all actions associated with this group action.
        """
        for action in self.actions:
            action.cancel()
        self.cancelled = True
        self.save()
