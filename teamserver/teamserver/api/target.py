"""
    This module contains all 'Target' API functions.
"""
from mongoengine.errors import DoesNotExist

from ..utils import success_response, get_filtered_target, handle_exceptions
from ..models import Target, Action, Group
from ..exceptions import CannotRenameTarget

@handle_exceptions
def create_target(params):
    """
    This API function creates a new target object in the database.

    name (required, unique): The name given to the target. <str>
    mac_addrs (required, unique): The MAC addresses used to identify the target. <[str, str]>
    facts (optional): A dictionary of key,value pairs to store for the target. <dict>
    """
    name = params['name']
    mac_addrs = params['mac_addrs']
    facts = params.get('facts', {})

    target = Target(
        name=name,
        mac_addrs=mac_addrs,
        facts=facts
    )
    target.save(force_insert=True)

    return success_response()

@handle_exceptions
def get_target(params):
    """
    This API function queries and returns a target object with the given name.

    name (required): The name of the target to search for. <str>
    include_status (optional): Should status be included, default: True. <bool>
    include_facts (optional): Should facts be included, default: False. <bool>
    include_sessions (optional): Should sessions be included, default: False. <bool>
    include_credentials (optional): Should credentials be included, default: False. <bool>
    include_actions (optional): Should actions be included, default: False. <bool>
    include_groups (optional): Should groups be included, default: False. <bool>
    """
    target = Target.get_by_name(params['name'])
    return success_response(target=get_filtered_target(target, params))

@handle_exceptions
def rename_target(params):
    """
    This API function will rename a target.

    name (required): The name of the target to search for. <str>
    new_name (required): The new name to assign the target. <str>
    """
    target = Target.get_by_name(params['name'])
    new_name = params['new_name']

    try:
        Target.get_by_name(new_name)
        raise CannotRenameTarget('Target with new_name already exists.')
    except DoesNotExist:
        pass

    for session in target.sessions:
        session.target_name = new_name
        session.save()

    for action in Action.get_target_actions(target.name):
        action.target_name = new_name
        action.save()

    for group in Group.get_target_groups(target.name):
        # TODO: Pull from whitelist, not dynamic members
        group.remove_member(target.name)
        group.whitelist_member(new_name)
        group.save()

    target.name = new_name
    target.save()

    return success_response()

@handle_exceptions
def set_target_facts(params):
    """
    This API function updates the facts dictionary for a target.
    It will overwrite any currently existing keys, but will not remove
    existing keys that are not specified in the 'facts' parameter.

    name (required): The name of the target to update. <str>
    facts (required): The dictionary of facts to use. <dict>
    """
    target = Target.get_by_name(params['name'])

    target.set_facts(params['facts'])

    return success_response(target={'name': target.name, 'facts': target.facts})

@handle_exceptions
def list_targets(params): #pylint: disable=unused-argument
    """
    This API function will return a list of target documents.

    include_status (optional): Should status be included, default: True. <bool>
    include_facts (optional): Should facts be included, default: False. <bool>
    include_sessions (optional): Should sessions be included, default: False. <bool>
    include_credentials (optional): Should credentials be included, default: False. <bool>
    include_actions (optional): Should actions be included, default: False. <bool>
    include_groups (optional): Should groups be included, default: False. <bool>
    """
    return success_response(targets={
        target.name: get_filtered_target(target, params) for target in Target.list_targets()
    })
