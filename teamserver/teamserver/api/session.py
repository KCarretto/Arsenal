"""
    This module contains all 'Session' API functions.
"""
import time

from uuid import uuid4
from mongoengine.errors import DoesNotExist

from .utils import success_response
from ..exceptions import handle_exceptions, UnattachedException
from ..models import Target, Session, SessionHistory, Action, Response, log
from ..config import DEFAULT_AGENT_SERVERS, DEFAULT_AGENT_INTERVAL
from ..config import DEFAULT_AGENT_INTERVAL_DELTA, DEFAULT_AGENT_CONFIG_DICT

@handle_exceptions
def create_session(params):
    """
    This API function creates a new session object in the database.

    mac_addrs (required): The list of MAC addresses that the agent gathered from the target <str>
    servers (optional): Which servers the agent will initially be configured with. <[str, str]>
    interval (optional): The interval the agent will initially be configured with. <float>
    interval_delta (optional): The interval delta the agent will initially be
                               configured with. <float>
    config_dict (optional): Any other configuration options that the agent is initially
                            configured with. <dict>
    facts (optional): An optional facts dictionary to update the target with.
    """
    # Fetch Target, create it automatically if it does not exist
    try:
        target = Target.get_by_macs(params['mac_addrs'])
    except DoesNotExist:
        target = Target(
            name=str(uuid4()),
            mac_addrs=params['mac_addrs'],
        )
        target.save(force_insert=True)

    # Create Session and SessionHistory documents
    session = Session(
        session_id=str(uuid4()),
        timestamp=time.time(),
        target_name=target.name,
        servers=params.get('servers', DEFAULT_AGENT_SERVERS),
        interval=params.get('interval', DEFAULT_AGENT_INTERVAL),
        interval_delta=params.get('interval_delta', DEFAULT_AGENT_INTERVAL_DELTA),
        config_dict=params.get('config_dict', DEFAULT_AGENT_CONFIG_DICT)
    )
    session_history = SessionHistory(
        session_id=session.session_id,
        checkin_timestamps=[session.timestamp]
    )
    session_history.save(force_insert=True)
    session.save(force_insert=True)

    # Update Target facts if they were included
    facts = params.get('facts')
    if facts and isinstance(facts, dict):
        target.set_facts(facts)

    log(
        'INFO',
        'New Session on (target: {}) (session: {})'.format(target.name, session.session_id))

    # TODO: Queue default config action

    return success_response(session_id=session.session_id)

@handle_exceptions
def get_session(params):
    """
    This API function queries and returns a session object with the given session_id.

    session_id (required): The session_id to search for. <str>
    """
    session = Session.get_by_id(params['session_id'])
    return success_response(session=session.document)

@handle_exceptions
def session_check_in(params): #pylint: disable=too-many-locals
    """
    This API function checks in a session, updating timestamps and history, submitting
    action responses, and will return new actions for the session to complete.

    session_id (required): The session_id of the session to check in. <str>
    responses (optional): Any responses to actions that the session is submitting. <[dict, dict]>
    facts (optional): Any updates to the Target's fact collection. <dict>
    config (optional): Any updates to the Session's config. <dict>
    """
    # Fetch session object, create one if it does not exist
    session = Session.get_by_id(params['session_id'])

    log(
        'INFO',
        'Session checked in from (target: {}) (session: {})'.format(
            session.target_name,
            session.session_id))

    # Update timestamps
    session.update_timestamp(time.time())

    # Submit responses
    responses = params.get('responses')
    responses = responses if responses else []
    for response in responses:
        action = Action.get_by_id(response['action_id'])

        if response['stderr'] is None:
            response['stderr'] = ''

        resp = Response(
            stdout=response['stdout'],
            stderr=response['stderr'],
            start_time=response['start_time'],
            end_time=response['end_time'],
            error=response['error'],
        )

        action.submit_response(resp)

    # TODO: Implement locking to avoid duplication

    # Gather new actions
    actions_raw = Action.get_target_unassigned_actions(session.target_name)
    actions = []
    # Assign each action to this status, and append it's document to the list
    priority = 0
    for action in sorted(actions_raw, key=lambda action: action.queue_time):
        action.assign_to(session)
        doc = action.agent_document
        doc['priority'] = priority
        actions.append(doc)
        priority += 1
    # TODO: Look for 'upload' actions and read file from disk

    # Update config if it was included
    config = params.get('config')
    if config and isinstance(config, dict):
        interval = config.get('interval')
        interval_delta = config.get('interval_delta')
        servers = config.get('servers')
        session.update_config(interval, interval_delta, servers, config)

    # Update facts if they were included
    facts = params.get('facts')
    if facts and isinstance(facts, dict):
        try:
            target = Target.get_by_name(session.target_name)
            target.set_facts(facts)
        except DoesNotExist:
            raise UnattachedException("Target for session does not exist.")

    # Respond
    return success_response(session_id=session.session_id, actions=actions)

@handle_exceptions
def update_session_config(params):
    """
    This API function updates the config dictionary for a session.
    It will overwrite any currently existing keys, but will not remove
    existing keys that are not specified in the 'config' parameter.

    NOTE: This should only be called when a session's config HAS been updated.
          to update a session's config, queue an action of type 'config'.

    session_id (required): The session_id of the session to update. <str>
    config_dict (optional): The config dictionary to use. <dict>
    servers (optional): The session's new servers. <[str, str]>
    interval (optional): The session's new interval. <float>
    interval_delta (optional): The session's new interval_delta. <float>
    """
    session = Session.get_by_id(params['session_id'])

    session.update_config(
        params.get('interval'),
        params.get('interval_delta'),
        params.get('servers'),
        params.get('config_dict')
    )

    return success_response(config=session.config)

@handle_exceptions
def list_sessions(params): #pylint: disable=unused-argument
    """
    This API function will return a list of session documents.
    It is highly recommended to avoid using this function, as it
    can be very expensive.
    """
    sessions = Session.list()
    return success_response(sessions={session.session_id: session.document for session in sessions})
