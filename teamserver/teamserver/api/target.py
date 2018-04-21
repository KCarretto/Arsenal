"""
    This module contains all 'Target' API functions.
"""
from flask import current_app
from mongoengine.errors import DoesNotExist

import teamserver.events.worker as events

from ..utils import success_response, get_filtered_target, handle_exceptions
from ..models import Target, Credential, Action, Group
from ..exceptions import CannotRenameTarget, MembershipError

@handle_exceptions
def create_target(params):
    """
    ### Overview
    This API function creates a new target object in the database.

    ### Parameters
    name (unique):      The name given to the target. <str>
    uuid (unique):      The unique identifier of the target. <str>
    facts (optional):   A dictionary of key,value pairs to store for the target. <dict>
    """
    name = params['name']
    uuid = params['uuid']
    facts = params.get('facts', {})

    target = Target(
        name=name,
        uuid=uuid,
        facts=facts
    )
    target.save(force_insert=True)

    # Generate Event
    if not current_app.config.get('DISABLE_EVENTS', False):
        events.trigger_event.delay(
            event='target_create',
            target=target.document(True, True, True),
        )

    return success_response()

@handle_exceptions
def get_target(params):
    """
    ### Overview
    This API function queries and returns a target object with the given name.

    ### Parameters
    name:                           The name of the target to search for. <str>
    include_status (optional):      Should status be included, default: True. <bool>
    include_facts (optional):       Should facts be included, default: False. <bool>
    include_sessions (optional):    Should sessions be included, default: False. <bool>
    include_credentials (optional): Should credentials be included, default: False. <bool>
    include_actions (optional):     Should actions be included, default: False. <bool>
    include_groups (optional):      Should groups be included, default: False. <bool>
    """
    target = Target.get_by_name(params['name'])
    return success_response(target=get_filtered_target(target, params))

@handle_exceptions
def rename_target(params):
    """
    ### Overview
    This API function will rename a target.

    ### Parameters
    name:       The name of the target to search for. <str>
    new_name:   The new name to assign the target. <str>
    """
    target = Target.get_by_name(params['name'])
    new_name = params['new_name']

    try:
        Target.get_by_name(new_name)
        raise CannotRenameTarget('Target with new_name already exists.')
    except DoesNotExist:
        pass

    sessions = []
    for session in target.sessions:
        session.target_name = new_name
        sessions.append(session)

    actions = []
    for action in Action.get_target_actions(target.name):
        action.target_name = new_name
        actions.append(action)

    groups = []
    for group in Group.get_target_groups(target.name):
        try:
            # Update explicit membership
            if target.name in group.whitelist_members:
                group.whitelist_members = [
                    name if name != target.name else new_name for name in group.whitelist_members
                ]
            elif target.name in group.blacklist_members:
                group.blacklist_members = [
                    name if name != target.name else new_name for name in group.blacklist_members
                ]

            # Update dynamic membership
            group.built_members = [
                name if name != target.name else new_name for name in group.built_members
            ]

            groups.append(group)

        except MembershipError:
            pass

    target.name = new_name
    target.save()

    for session in sessions:
        session.save()
    for action in actions:
        action.save()
    for group in groups:
        group.save()

    # Generate Event
    if not current_app.config.get('DISABLE_EVENTS', False):
        events.trigger_event.delay(
            event='target_rename',
            old_name=params['name'],
            new_name=new_name,
        )

    return success_response()

@handle_exceptions
def set_target_facts(params):
    """
    This API function updates the facts dictionary for a target.
    It will overwrite any currently existing keys, but will not remove
    existing keys that are not specified in the 'facts' parameter.

    name: The name of the target to update. <str>
    facts: The dictionary of facts to use. <dict>
    """
    target = Target.get_by_name(params['name'])

    target.set_facts(params['facts'])

    return success_response(target={'name': target.name, 'facts': target.facts})

@handle_exceptions
def list_targets(params): #pylint: disable=unused-argument
    """
    This API function will return a list of target documents.

    include_status (optional):      Should status be included, Default: True. <bool>
    include_facts (optional):       Should facts be included, Default: False. <bool>
    include_sessions (optional):    Should sessions be included, Default: False. <bool>
    include_credentials (optional): Should credentials be included, Default: False. <bool>
    include_actions (optional):     Should actions be included, Default: False. <bool>
    include_groups (optional):      Should groups be included, Default: False. <bool>
    """
    return success_response(targets={
        target.name: get_filtered_target(target, params) for target in Target.list_targets()
    })

@handle_exceptions
def migrate_target(params):
    """
    ### Overview
    This API function will move all sessions from one target, to another. It will then delete the
    old target and rename the new target after the old one.

    ### Parameters
    old_target: The name of the outdated target. <str>
    new_target: The name of the new target to migrate to. <str>
    """
    old_target = Target.get_by_name(params['old_target'])
    new_target = Target.get_by_name(params['new_target'])

    new_name = old_target.name

    # Delete old target
    old_target.remove()

    # Rename new target
    rename_target({
        'name': new_target.name,
        'new_name': new_name
    })

    return success_response()

@handle_exceptions
def add_credentials(params):
    """
    ### Overview
    This API function associates valid credentials with a target.

    ### Parameters
    target_name: The name of the target to associate credentials with.
    user: The user that the credentials are for.
    key: The secret key. This could be the password, or SSH key.
    service(optional): Optionally document what service this is for.
    """
    target = Target.get_by_name(params['target_name'])

    creds = Credential(
        target_name=target.name,
        user=params['user'],
        key=params['key'],
        service=params.get('service')
    )
    creds.save()

    return success_response()


@handle_exceptions
def invalidate_credentials(params):
    """
    ### Overview
    This API function invalidates a set of credentials.

    ### Parameters
    target_name: The name of the target to invalidate credentials for.
    user: The username for the credentials.
    key: The secret key for the credentials.
    """
    cred = Credential.objects.get( # pylint: disable=no-member
        target_name=params['target_name'],
        user=params['user'],
        key=params['key']
    )
    cred.valid = False
    cred.save()

    return success_response()

@handle_exceptions
def list_credentials(params):
    """
    ### Overview
    This API function is used to list valid credentials for a target.

    ### Parameters
    target_name: The name of the target to list credentials for.
    """
    target = Target.get_by_name(params['target_name'])

    return success_response(
        credentials=[creds.document for creds in target.credentials]
    )
