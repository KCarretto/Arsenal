"""
    This module contains all 'GroupAction' API functions.
"""
from uuid import uuid4
from .utils import success_response
from ..models import GroupAction, Group
from .action import create_action

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
