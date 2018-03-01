"""
    This module serves as the entry point for all basic API calls.
    It passes appropriate parameter information to various other modules,
    that will do the heavy lifting.
"""

from flask import Blueprint, request, jsonify
from .api.target import create_target, get_target, set_target_facts, list_targets

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

@API.route('/', methods=['POST'])
@API.route('/api', methods=['POST'])
@API.route('/api/v1', methods=['POST'])
def api_entry():
    """
    This function serves as the entry point for the v1 JSON API.
    """
    data = request.get_json()
    if data is None:
        data = request.form

    # Available methods
    api_functions = {
        # Web Hooks
        'RegisterWebhook': None,
        'RemoveWebhook': None,
        'ListWebhooks': None,

        # API Tokens
        'CreateAPIToken': None,
        'DeleteAPIToken': None,

        # Targets
        'CreateTarget': create_target,
        'GetTarget': get_target,
        'SetTargetFacts': set_target_facts,
        'ArchiveTarget': None,
        'ListTargets': list_targets,

        # Sessions
        'CreateSession': None,
        'GetSession': None,
        'SessionCheckIn': None,
        'UpdateSessionConfig': None,
        'ArchiveSession': None,
        'ListSessions': None,

        # Actions
        'CreateAction': None,
        'GetAction': None,
        'CancelAction': None,
        'ListActions': None,

        # Group Actions
        'CreateGroupAction': None,
        'GetGroupAction': None,
        'CancelGroupAction': None,
        'ListGroupActions': None,

        # Groups
        'CreateGroup': None,
        'GetGroup': None,
        'AddGroupMembers': None,
        'RemoveGroupMembers': None,
        'ListGroups': None,
        'DeleteGroup': None,

        # Credentials
        'CreateCredentials': None,
        'GetValidCredentials': None,
        'InvalidateCredentials': None,
        'ListCredentials': None,

        # Logs
        'CreateLog': None,
        'ListLogs': None
    }

    # Attempt to find method
    method = None
    try:
        method = api_functions[data['method']]
    except KeyError:
        # Return method not found
        return jsonify({
            'status': 404,
            'description': 'Method not found.',
            'error': True
        })

    # If method was found but is None, return not implemented
    if method is None or not callable(method):
        return jsonify({
            'status': 501,
            'description': 'Method not implemented.',
            'error': True
        })

    # Peform auth check, ensure user has permissions
    # TODO: Enable Authentication

    # Trigger method pre-hooks
    # TODO: Trigger method pre-hooks

    # Call method
    response = method(data)

    # Trigger method post-hooks
    # TODO: Trigger method post-hooks

    # Return method output
    return jsonify(response)

