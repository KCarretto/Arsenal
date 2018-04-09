"""
    This module defines a python object model for the Group document
    in the backend MongoDB database.
"""
import re

from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import StringField
from mongoengine.fields import ListField, EmbeddedDocumentListField

from .target import Target

from ..config import MAX_STR_LEN
from ..config import COLLECTION_GROUPS

from ..exceptions import MembershipError

class GroupAutomemberRule(EmbeddedDocument):
    """
    This class represents an embedded document into the group document,
    which will be used to calculate members of a group.
    """
    rule_id = StringField(required=True, null=False, unique=True, max_length=MAX_STR_LEN)
    attribute = StringField(required=True, null=False, max_length=MAX_STR_LEN)
    regex = StringField(required=True, null=False, max_length=MAX_STR_LEN)

    @property
    def document(self):
        """
        Return formatted json for the object.
        """
        return {
            'rule_id': self.rule_id,
            'attribute': self.attribute,
            'regex': self.regex,
        }

class Group(Document):
    """
    This class represents a collection of target systems. Some are
    added to the group manually, while some are dynamically added
    based on group membership rules.
    """
    meta = {
        'collection': COLLECTION_GROUPS,
        'indexes': [
            {
                'fields': ['name'],
                'unique': True
            }
        ]
    }
    name = StringField(required=True, null=False, unique=True)

    built_members = ListField(StringField(required=True, null=False))
    whitelist_members = ListField(StringField(required=True, null=False))
    blacklist_members = ListField(StringField(required=True, null=False))

    membership_rules = EmbeddedDocumentListField(GroupAutomemberRule, null=False)

    @staticmethod
    def get_target_groups(target_name):
        """
        WARNING: Expensive Method
        This method returns a list of groups that a target is in.
        """
        groups = []
        for group in Group.objects(): #pylint: disable=no-member
            if target_name in group.members:
                groups.append(group)

        return list(set(groups))

    @staticmethod
    def get_by_name(name):
        """
        This method queries for the group with the given name.
        """
        return Group.objects.get(name=name) #pylint: disable=no-member

    @staticmethod
    def list_groups():
        """
        This method queries for all group objects.
        """
        return Group.objects() #pylint: disable=no-member

    @property
    def members(self):
        """
        This property returns member objects of all group members.
        """
        if not self.built_members:
            self.build_members()

        return self.built_members

    @property
    def document(self):
        """
                This property filters and returns the JSON information for a queried group.
        """
        return {
            'name': self.name,
            'members': self.members,
            'whitelist_members': self.whitelist_members,
            'blacklist_members': self.blacklist_members,
            'rules': [rule.document for rule in self.membership_rules], # pylint: disable=not-an-iterable
        }

    def whitelist_member(self, target_name):
        """
        This function attempts to add a target to the member whitelist.
        The target will not be added if the target is in the blacklist.
        """

        if target_name in self.blacklist_members: #pylint: disable=unsupported-membership-test
            raise MembershipError('Cannot whitelist a member that is on the blacklist.')

        self.whitelist_members.append(target_name) #pylint: disable=no-member
        self.build_members()

    def remove_member(self, target_name):
        """
        This function removes a target from the member whitelist.
        """
        if not target_name in self.whitelist_members: #pylint: disable=unsupported-membership-test
            raise MembershipError('Cannot remove member, member is not whitelisted.')
        self.whitelist_members.remove(target_name) #pylint: disable=no-member
        self.build_members()

    def blacklist_member(self, target_name):
        """
        This function removes a target from the member whitelist (if they exist),
        and add them to the blacklist (if they are not yet on there).
        """
        try:
            self.remove_member(target_name)
        except ValueError:
            pass

        if target_name in self.blacklist_members: #pylint: disable=unsupported-membership-test
            raise MembershipError('Member is already blacklisted.')
        self.blacklist_members.append(target_name) #pylint: disable=no-member
        self.build_members()

    def remove(self):
        """
        Remove this document from the database, and perform any related cleanup.
        """
        self.delete()

    def build_members(self):
        """
        Determine group members.
        """
        targets = []

        def get_value(value, attributes):
            """
            Recursively look up values based on tokens.
            """
            if attributes:
                if hasattr(value, attributes[0]):
                    value = getattr(value, attributes[0])
                    return get_value(value, attributes[1:])
                elif isinstance(value, dict) and value.get(attributes[0]):
                    value = value[attributes[0]]
                    return get_value(value, attributes[1:])
            return value

        # Filter through objects and compute regexes
        if self.membership_rules:
            for target in Target.objects: # pylint: disable=no-member
                for rule in self.membership_rules: # pylint: disable=not-an-iterable
                    pattern = re.compile(rule.regex)
                    value = get_value(target, rule.attribute.split('.')) # pylint: disable=no-member
                    if pattern.match(str(value)):
                        targets.append(target.name)
                        break

        # Add whitelisted members
        targets += self.whitelist_members

        # Set compiled list of members
        self.built_members = list(filter(lambda x: x not in self.blacklist_members, set(targets))) #pylint: disable=unsupported-membership-test
        self.save()
