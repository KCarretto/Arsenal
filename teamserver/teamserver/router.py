"""
    This module serves as the entry point for all basic API calls.
    It passes appropriate parameter information to various other modules,
    that will do the heavy lifting.
"""

from flask import Blueprint, request, jsonify, current_app

import teamserver.events as events

from .api import create_target, get_target, rename_target
from .api import set_target_facts, list_targets, migrate_target
from .api import create_session, get_session, session_check_in
from .api import update_session_config, list_sessions
from .api import create_action, get_action, cancel_action, list_actions
from .api import create_group_action, get_group_action, cancel_group_action, list_group_actions
from .api import get_group, create_group, delete_group, list_groups
from .api import remove_group_member, add_group_member, blacklist_group_member
from .api import create_log, list_logs
from .api import register_agent, get_agent, list_agents, unregister_agent
from .api import create_user, create_role, create_api_key
from .api import get_user, get_role, get_current_context
from .api import update_role_permissions, update_user_password
from .api import add_role_member, remove_role_member
from .api import list_api_keys, list_roles, list_users
from .api import delete_role, delete_user, revoke_api_key
from .api import register_webhook, unregister_webhook, list_webhooks
from .models import APIKey, User
from .utils import authenticate, respond, log

API = Blueprint('router', __name__)

@API.route('/status')
def teamserver_status():
    """
    This endpoint returns the current status of the teamserver.
    """
    return jsonify(
        {
            'status': 200,
            'state': 'Running',
            'error': False
        }
    )

@API.route('/api/login', methods=['POST'])
@API.route('/api/v1/login', methods=['POST'])
def login():
    """
    This endpoint can be used to authenticate a User or API key.
    It will return a session token in the Set-Cookie header as well as in the JSON response,
    that has the same permissions as the User or API key that was used to authenticate.
    The session token will expire, and then the user will need to reauthenticate.
    """
    valid, response = authenticate(request)
    if not valid:
        return respond(response)
    # TODO: Create session token
    # TODO: Set-Cookie session token
    return respond({
        'status': 200,
        'error': False,
        'session_token': None
    })

@API.route('/', methods=['POST'])
@API.route('/api', methods=['POST'])
@API.route('/api/v1', methods=['POST'])
def api_entry(): # pylint: disable=too-many-return-statements
    """
    This function serves as the entry point for the v1 JSON API.
    """
    data = request.get_json()
    if data is None:
        data = request.form

    # Available methods
    api_functions = {
        # Web Hooks
        'RegisterWebhook': register_webhook,
        'UnregisterWebhook': unregister_webhook,
        'ListWebhooks': list_webhooks,

        # Targets
        'CreateTarget': create_target,
        'GetTarget': get_target,
        'SetTargetFacts': set_target_facts,
        'RenameTarget': rename_target,
        'ListTargets': list_targets,
        'MigrateTarget': migrate_target,

        # Sessions
        'CreateSession': create_session,
        'GetSession': get_session,
        'SessionCheckIn': session_check_in,
        'UpdateSessionConfig': update_session_config,
        'ArchiveSession': None,
        'ListSessions': list_sessions,

        # Actions
        'CreateAction': create_action,
        'GetAction': get_action,
        'CancelAction': cancel_action,
        'ListActions': list_actions,

        # Group Actions
        'CreateGroupAction': create_group_action,
        'GetGroupAction': get_group_action,
        'CancelGroupAction': cancel_group_action,
        'ListGroupActions': list_group_actions,

        # Groups
        'CreateGroup': create_group,
        'GetGroup': get_group,
        'AddGroupMember': add_group_member,
        'RemoveGroupMember': remove_group_member,
        'BlacklistGroupMember': blacklist_group_member,
        'DeleteGroup': delete_group,
        'ListGroups': list_groups,

        # Credentials
        'CreateCredentials': None,
        'GetValidCredentials': None,
        'InvalidateCredentials': None,
        'ListCredentials': None,

        # Logs
        'CreateLog': create_log,
        'ListLogs': list_logs,

        # Agents
        'RegisterAgent': register_agent,
        'GetAgent': get_agent,
        'ListAgents': list_agents,
        'UnregisterAgent': unregister_agent,

        # Auth
        'CreateUser': create_user,
        'CreateAPIKey': create_api_key,
        'CreateRole': create_role,

        'GetUser': get_user,
        'GetRole': get_role,
        'GetCurrentContext': get_current_context,

        'UpdateUserPassword': update_user_password,
        'UpdateRolePermissions': update_role_permissions,

        'AddRoleMember': add_role_member,
        'RemoveRoleMember': remove_role_member,

        'ListUsers': list_users,
        'ListRoles': list_roles,
        'ListAPIKeys': list_api_keys,

        'DeleteUser': delete_user,
        'RevokeAPIKey': revoke_api_key,
        'DeleteRole': delete_role,

        #'KillSession': kill_session,
        #'KillSessions': kill_sessions,
    }

    # Attempt to find method
    method = None
    try:
        method = api_functions[data['method']]
    except KeyError:
        # Return method not found
        return respond({
            'status': 404,
            'description': 'Method not found.',
            'error_type': 'method-not-found',
            'error': True
        })

    # If method was found but is None, return not implemented
    if method is None or not callable(method):
        return respond({
            'status': 501,
            'description': 'Method not implemented.',
            'error_type': 'method-not-implemented',
            'error': True
        })

    # Allow DISABLE_AUTH debug setting for unit tests
    if current_app.config.get('DISABLE_AUTH', False):
        log('WARN', 'Authentication and authorization have been disabled by application setting.')
        log('DEBUG', 'Calling API method {}'.format(data['method']))
        return respond(method(data))

    # Peform authentication check
    valid, response = authenticate(request)
    if not valid:
        return respond(response)

    # Perform authorization check
    # Ensure the response we recieved is a valid auth object
    if isinstance(response, (User, APIKey)) and response.is_permitted(data['method']):

        username = None

        # Generate a DEBUG log message
        if isinstance(response, User):
            username = response.username
            log('DEBUG', '{} calling API method {}'.format(username, data['method']))
        else:
            username = response.owner
            log('DEBUG', '{} calling API method {} using API Key'.format(
                username,
                data['method']))

        # Trigger method pre-hooks
        if not current_app.config.get('DISABLE_EVENTS', False):
            events.trigger_event.delay(
                event='api_call',
                method=data['method'],
                user=username,
            )

        # Override the reserved 'arsenal_auth_object' field with the given auth object
        data['arsenal_auth_object'] = response

        # Call the API function, passing the received JSON
        return respond(method(data))
    else:
        return respond({
            'status': 403,
            'error': True,
            'error_type': 'permission-denied',
            'description': 'Permission Denied.',
        })

    return respond({
        'status': 500,
        'error': True,
        'description': 'An unknown error occurred.',
        'error_type': 'unknown-error',
    })
