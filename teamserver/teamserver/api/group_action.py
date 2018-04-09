"""
    This module contains all 'GroupAction' API functions.
"""
from uuid import uuid4

from ..utils import success_response, handle_exceptions, log, get_context
from .action import create_action
from ..models import GroupAction, Group

@handle_exceptions
def create_group_action(params):
    """
    Creates an action and assigns it to a group of targets. Each target
    will complete the action, and the statuses of each action will be
    easily accessible through the created group action document.

    group_name (required): The name of the group to create an action for.
    action_string (required): The action to perform on the targets.
    """
    username = 'No owner'

    try:
        user, _, _ = get_context(params)
        if user:
            username = user.username
    except KeyError:
        pass

    action_string = params['action_string']
    group_name = params['group_name']
    actions = []

    # Iterate through all desired targets
    for target_name in Group.get_by_name(group_name).members:
        # Invoke the API to create action objects without commiting to the database.
        action = create_action({
            'target_name': target_name,
            'action_string': action_string
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
        action_string=action_string,
        action_ids=action_ids,
        owner=username,
    )
    group_action.save(force_insert=True)
    log(
        'INFO',
        'Group Action Created (action: {}) on (group: {})'.format(action_string, group_name))

    # Return successful response including the group_action_id for tracking
    return success_response(group_action_id=group_action.group_action_id)

@handle_exceptions
def get_group_action(params):
    """
    Retrieves a group action from the database based on the group_action_id.

    group_action_id: The group action identifier to query for.
    """
    group_action = GroupAction.get_by_id(params['group_action_id'])

    return success_response(group_action=group_action.document)

@handle_exceptions
def cancel_group_action(params):
    """
    Cancels all actions associated with a group action (only if status is queued).

    group_action_id: The unique identifier associated with the group action. <str>
    """
    group_action = GroupAction.get_by_id(params['group_action_id'])
    group_action.cancel()

    return success_response()

@handle_exceptions
def list_group_actions(params): #pylint: disable=unused-argument
    """
    This API function will return a list of group action documents.
    It is highly recommended to avoid using this function, as it
    can be very expensive.
    """
    group_actions = GroupAction.list_group_actions()
    return success_response(group_actions={
        group_action.group_action_id: group_action.document for group_action in group_actions})
