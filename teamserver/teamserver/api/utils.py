"""
    This module provides utillity functions accessible by all API modules.
"""
from ..models import Action, Group

def success_response(**kwargs):
    """
    This function will generate a dictionary with generic successful
    response keys, as well as any key value pairs provided.
    """
    response = {}

    for key, value in kwargs.items():
        response[key] = value

    response['status'] = 200
    response['error'] = False

    return response

def _get_filtered_target(target, params):
    """
    Return a filtered target document based on includes.
    """
    doc = target.document(
        params.get('include_status', True),
        params.get('include_facts', False),
        params.get('include_sessions', False),
        params.get('include_credentials', False)
    )
    if params.get('include_actions', False):
        doc['actions'] = [action.document for action in Action.get_target_actions(target.name)]
    if params.get('include_groups', False):
        doc['groups'] = [group.document for group in Group.get_target_groups(target.name)]
    return doc
