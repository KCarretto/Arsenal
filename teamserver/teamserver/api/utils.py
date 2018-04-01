"""
    This module provides utillity functions accessible by all API modules.
"""
from ..models import Action, Group, User, APIKey

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

def _get_user(params):
    """
    Returns a user object based on the arsenal_auth_object.
    """
    # Retrieve current authentication context
    auth_obj = params['arsenal_auth_object']

    # Lookup user object if authentication object was an API key
    user = params['arsenal_auth_object']
    if isinstance(auth_obj, APIKey):
        user = User.get_user(auth_obj.owner)

    # Return allowed_api_calls to prevent API keys from assuming user permissions
    return (user, auth_obj.allowed_api_calls)

def _get_context(params):
    """
    Allow administrative users to assume another user context.
    """
    user, allowed_methods = _get_user(params)
    administrator = user.administrator
    # Allow administrators to override the owner with a custom value
    if params.get('user_context') and administrator:
        # Change the operating user context
        user = User.get_user(params['user_context'])
        allowed_methods = user.allowed_api_calls

    return (user, allowed_methods, administrator)

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
