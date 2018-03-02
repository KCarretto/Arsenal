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

    target_name (required): The name of the target to perform the action on.
    action_string (required): The action string that will be parsed into an action.
    bound_session_id (optional): This will restrict the action to only be retrieved
                                 by a specific session.
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

    return success_response()
#
#
#def get_action(params):
#    pass
#
#def cancel_actions(params):
#    pass
#
#def list_actions(params):
#    pass
