"""
    This module contains all 'Action' API functions.
"""
from uuid import uuid4

import time

from .utils import success_response
from ..models.action import Action

def create_action(params):
    """
    This API function creates a new action object in the database.

    target_name (required): The name of the target to perform the action on. <str>
    action_string (required): The action string that will be parsed into an action. <str>
    bound_session_id (optional): This will restrict the action to only be retrieved
                                 by a specific session. <str>
    """
    target_name = params['target_name']
    action_string = params['action_string']
    bound_session_id = params.get('bound_session_id')

    parsed_action = Action.parse_action_string(action_string)

    action = Action(
        action_id=str(uuid4()),
        target_name=target_name,
        action_string=action_string,
        action_type=parsed_action['action_type'],
        bound_session_id=bound_session_id,
        queue_time=time.time()
    )
    for key, value in parsed_action.items():
        if key not in [
                'action_id',
                'target_name',
                'action_string',
                'action_type',
                'bound_session_id',
                'queue_time',
                'sent_time',
                'complete_time',
                'response'
        ]:
            action.__setattr__(key, value)
    action.save(force_insert=True)

    return success_response(action_id=action.action_id)

def get_action(params):
    """
    Retrieves an action from the database based on action_id.

    action_id: The action_id of the action to query for. <str>
    """
    action = Action.get_by_id(params['action_id'])

    return success_response(action=action.document)

def cancel_action(params):
    """
    Cancels an action if it has not yet been sent.
    This will prevent sessions from retrieving it.

    action_id: The action_id of the action to cancel. <str>
    """
    action = Action.get_by_id(params['action_id'])
    if not action.cancel():
        # TODO: Raise exception to return error response
        pass

    return success_response()

def list_actions(params): #pylint: disable=unused-argument
    """
    This API function will return a list of action documents.
    It is highly recommended to avoid using this function, as it
    can be very expensive.
    """
    actions = Action.list()
    return success_response(actions={action.action_id: action.document for action in actions})
