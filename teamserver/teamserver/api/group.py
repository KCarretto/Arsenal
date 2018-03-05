"""
    This module contains all 'Group' API functions.
"""
from .utils import success_response
from ..models.group import Group
from ..models.target import Target

def create_group(params):
    """
    This function creates a group object in the database.

    name (required, unique): A unique and human readable identifier for the group. <str>
    """
    name = params['group_name']

    group = Group(
        name=name
    )
    group.save(force_insert=True)

    return success_response()

def get_group(params):
    """
    Retrieves a group from the database based on name.

    name: The name of the group to query for. <str>
    """
    group = Group.get_by_name(params['name'])

    return success_response(group=group.document)

def add_group_member(params):
    """
    This whitelists a member into a group. This means that
    regardless of properties, the member will be a part of the
    group.

    group_name: The name of the group to modify. <str>
    target_name: The name of the member to add. <str>
    """
    group = Group.get_by_name(params['group_name'])
    target = Target.get_by_name(params['target_name'])

    group.whitelist_member(target)

    return success_response()

def remove_group_member(params):
    """
    Removes a target from a group's membership whitelist.

    group_name: The name of the group to modify. <str>
    target_name: The name of the member to remove. <str>
    """
    group = Group.get_by_name(params['group_name'])
    target = Target.get_by_name(params['target_name'])

    group.remove_group_member(target)

    return success_response()

def blacklist_group_member(params):
    """
    Blacklist a target from ever being a member of a group.

    group_name: The name of the group to modify. <str>
    target_name: The name of the member to remove. <str>
    """
    group = Group.get_by_name(params['group_name'])
    target = Target.get_by_name(params['target_name'])

    group.blacklist_member(target)

    return success_response()

#def list_groups():
#    pass

#def delete_group():
#    pass
