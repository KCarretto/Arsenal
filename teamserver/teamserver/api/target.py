"""
    This module contains all 'Target' API functions.
"""
from .utils import success_response
from ..models import Target, Group
from ..exceptions import handle_exceptions

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

    name (required): The name of target to search for. <str>
    """
    target = Target.get_by_name(params['name'])

    return success_response(target=target.document)

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
    target.save()

    return success_response(target={'name': target.name, 'facts': target.facts})

@handle_exceptions
def list_targets(params): #pylint: disable=unused-argument
    """
    This API function will return a list of target documents.
    WARNING: It is highly recommended to avoid using this function, as it
    can be very expensive.
    """
    targets = Target.list()
    return success_response(targets={target.name: target.document for target in targets})

@handle_exceptions
def get_target_groups(params):
    """
    List which groups a target is in.

    name (required): The name of target to search for. <str>
    """
    target = Target.get_by_name(params['name'])
    return success_response(groups=[group.name for group in Group.target_groups(target.name)])
