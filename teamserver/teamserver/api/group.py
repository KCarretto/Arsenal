"""
    This module contains all 'Group' API functions.
"""
from uuid import uuid4

from ..utils import success_response, handle_exceptions
from ..models import Group, GroupAutomemberRule, Target

@handle_exceptions
def create_group(params):
    """
    ### Overview
    This function creates a group object in the database.

    ### Parameters
    name (unique):  A unique and human readable identifier for the group. <str>
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
    ### Overview
    Retrieves a group from the database based on name.

    ### Parameters
    name:   The name of the group to query for. <str>
    """
    group = Group.get_by_name(params['name'])
    return success_response(group=group.document)

@handle_exceptions
def add_group_member(params):
    """
    ### Overview
    This whitelists a member into a group. This means that
    regardless of properties, the member will be a part of the
    group.

    ### Parameters
    group_name:     The name of the group to modify. <str>
    target_name:    The name of the member to add. <str>
    """
    group = Group.get_by_name(params['group_name'])
    target = Target.get_by_name(params['target_name'])

    group.whitelist_member(target.name)

    return success_response()

@handle_exceptions
def remove_group_member(params):
    """
    ### Overview
    Removes a target from a group's membership whitelist.

    ### Parameters
    group_name:     The name of the group to modify. <str>
    target_name:    The name of the member to remove. <str>
    """
    group = Group.get_by_name(params['group_name'])
    target = Target.get_by_name(params['target_name'])

    group.remove_member(target.name)

    return success_response()

@handle_exceptions
def blacklist_group_member(params):
    """
    ### Overview
    Blacklist a target from ever being a member of a group.

    ### Parameters
    group_name:     The name of the group to modify. <str>
    target_name:    The name of the member to remove. <str>
    """
    group = Group.get_by_name(params['group_name'])
    target = Target.get_by_name(params['target_name'])

    group.blacklist_member(target.name)

    return success_response()

@handle_exceptions
def unblacklist_group_member(params):
    """
    ### Overview
    Remove a target from the blacklist of a group.

    ### Parameters
    group_name:     The name of the group to modify. <str>
    target_name:    The name of the member to remove. <str>
    """
    group = Group.get_by_name(params['group_name'])
    target = Target.get_by_name(params['target_name'])

    group.unblacklist_member(target.name)

    return success_response()

@handle_exceptions
def delete_group(params):
    """
    ### Overview
    Delete a group from the database.

    ### Parameters
    name:   The unique identifier for the group to delete. <str>
    """
    group = Group.get_by_name(params['name'])
    group.delete()
    return success_response()

@handle_exceptions
def list_groups(params): #pylint: disable=unused-argument
    """
    ### Overview
    List all groups that currently exist.
    WARNING: This will be quite an expensive operation.
    """
    groups = Group.list_groups()
    return success_response(groups={group.name: group.document for group in groups})

@handle_exceptions
def add_group_rule(params):
    """
    ### Overview
    Add a membership rule for the group.

    ### Parameters
    name:       The name of the group to modify. <str>
    attribute:  The attribute to build membership based on. You may access fields using
                    the '.' operator, for example: 'facts.interfaces'. Each attribute is
                    converted into a str for regex matching. <str>
    regex:      The inclusion regex, targets with matching attributes are included as
                    group members. <str>
    rule_id:    Optionally specify a unique name for the rule. <str>
    """
    rule = GroupAutomemberRule(
        attribute=params['attribute'],
        regex=params['regex'],
        rule_id=params.get('rule_id', str(uuid4())),
    )
    group = Group.get_by_name(params['name'])
    group.membership_rules.append(rule)
    group.build_members()

    return success_response(rule_id=rule.rule_id)

@handle_exceptions
def remove_group_rule(params):
    """
    ### Overview
    Remove an automembership rule for the group.

    ### Parameters
    name:       The name of the group to modify. <str>
    rule_id:    The unique identifier of the rule to remove. <str>
    """
    group = Group.get_by_name(params['name'])
    group.membership_rules = list(filter(
        lambda x: x.rule_id != params['rule_id'], group.membership_rules))
    group.build_members()

    return success_response()

@handle_exceptions
def rebuild_group_members(params):
    """
    ### Overview
    Recalculate group members.

    ### Parameters
    name (optional):    Optionally specify a single group to rebuild membership for. <str>
    """

    if params.get('name'):
        group = Group.get_by_name(params['name'])
        group.build_members()
    else:
        for group in Group.objects: # pylint: disable=no-member
            group.build_members()

    return success_response()
