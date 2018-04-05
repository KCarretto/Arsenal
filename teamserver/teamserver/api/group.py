"""
    This module contains all 'Group' API functions.
"""
from ..utils import success_response, handle_exceptions
from ..models import Group, Target

@handle_exceptions
def create_group(params):
    """
    This function creates a group object in the database.

    name (required, unique): A unique and human readable identifier for the group. <str>
    """
    name = params['name']

    group = Group(
        name=name
    )
    group.save(force_insert=True)

    return success_response()

@handle_exceptions
def get_group(params):
    """
    Retrieves a group from the database based on name.

    name: The name of the group to query for. <str>
    """
    group = Group.get_by_name(params['name'])
    return success_response(group=group.document)

@handle_exceptions
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

    group.whitelist_member(target.name)

    return success_response()

@handle_exceptions
def remove_group_member(params):
    """
    Removes a target from a group's membership whitelist.

    group_name: The name of the group to modify. <str>
    target_name: The name of the member to remove. <str>
    """
    group = Group.get_by_name(params['group_name'])
    target = Target.get_by_name(params['target_name'])

    group.remove_member(target.name)

    return success_response()

@handle_exceptions
def blacklist_group_member(params):
    """
    Blacklist a target from ever being a member of a group.

    group_name: The name of the group to modify. <str>
    target_name: The name of the member to remove. <str>
    """
    group = Group.get_by_name(params['group_name'])
    target = Target.get_by_name(params['target_name'])

    group.blacklist_member(target.name)

    return success_response()

@handle_exceptions
def delete_group(params):
    """
    Delete a group from the database.

    name: The unique identifier for the group to delete. <str>
    """
    group = Group.get_by_name(params['name'])
    group.delete()
    return success_response()

@handle_exceptions
def list_groups(params): #pylint: disable=unused-argument
    """
    List all groups that currently exist.
    WARNING: This will be quite an expensive operation.
    """
    groups = Group.list_groups()
    return success_response(groups={group.name: group.document for group in groups})
