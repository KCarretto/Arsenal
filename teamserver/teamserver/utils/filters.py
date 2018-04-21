"""
This module contains functionality that is designed to filter documents based on parameters.
"""
from ..models import Action, Group

def get_filtered_target(target, params):
    """
    Return a filtered target document based on includes.
    """
    doc = target.document(
        params.get('include_status', True),
        params.get('include_facts', False),
        params.get('include_sessions', False),
    )
    if params.get('include_actions', False):
        doc['actions'] = [action.document for action in Action.get_target_actions(target.name)]
    if params.get('include_groups', False):
        doc['groups'] = [group.document for group in Group.get_target_groups(target.name)]
    return doc
