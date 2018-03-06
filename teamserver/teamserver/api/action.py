"""
    This module contains all 'Action' API functions.
"""
from uuid import uuid4

import time

from .utils import success_response
from ..models.action import Action, GroupAction
from ..models.group import Group

def create_action(params, commit=True):
    """
    This API function creates a new action object in the database.

    target_name (required, unique): The name of the target to perform the action on. <str>
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

    action.update_fields(parsed_action)

    if commit:
        action.save(force_insert=True)
    else:
        return action

    return success_response(action_id=action.action_id)

def get_action(params):
    """
    Retrieves an action from the database based on action_id.

    action_id(required): The action_id of the action to query for. <str>
    """
    action = Action.get_by_id(params['action_id'])

    return success_response(action=action.document)

def cancel_action(params):
    """
    Cancels an action if it has not yet been sent.
    This will prevent sessions from retrieving it.

    action_id(required): The action_id of the action to cancel. <str>
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

def create_group_action(params):
    """
    Creates an action and assigns it to a group of targets. Each target
    will complete the action, and the statuses of each action will be
    easily accessible through the created group action document.

    group_name (required): The name of the group to create an action for.
    action_string (required): The action to perform on the targets.
    """

    actions = []

    # Iterate through all desired targets
    for target_name in Group.get_by_name(params['group_name']).member_names:
        # Invoke the API to create action objects without commiting to the database.
        action = create_action({
            'target_name': target_name,
            'action_string': params['action_string']
        }, False)

        actions.append(action)

    # Iterate through actions after each object has been successfully created
    action_ids = []
    for action in actions:
        action.save(force_insert=True)
        action_ids.append(action.action_id)

    # Create a group action document to track the actions
    group_action = GroupAction(
        group_action_id=str(uuid4()),
        action_string=params['action_string'],
        action_ids=action_ids
    )
    group_action.save(force_insert=True)

    # Return successful response including the group_action_id for tracking
    return success_response(group_action_id=group_action.group_action_id)

def get_group_action(params):
    """
    Retrieves a group action from the database based on the group_action_id.

    group_action_id: The group action identifier to query for.
    """
    group_action = GroupAction.get_by_id(params['group_action_id'])

    return success_response(group_action=group_action.document)
