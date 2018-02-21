"""
    This module defines a python object model for the Group document
    in the backend MongoDB database.
"""

from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import BooleanField, StringField
from mongoengine.fields import ListField, EmbeddedDocumentListField

from .target import Target

from ..config import MAX_STR_LEN
from ..config import COLLECTION_GROUPS

class GroupAutomemberRule(EmbeddedDocument):
    """
    This class represents an embedded document into the group document,
    which will be used to calculate members of a group.
    """
    property = StringField(required=True, null=False, max_length=MAX_STR_LEN)
    regex = StringField(required=True, null=False, max_length=MAX_STR_LEN)
    include = BooleanField(required=True, null=False, default=True)

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

    whitelist_members = ListField(StringField(required=True, null=False), required=True, null=False)
    blacklist_members = ListField(StringField(required=True, null=False), required=True, null=False)

    membership_rules = EmbeddedDocumentListField(GroupAutomemberRule(null=False), null=False)

    @staticmethod
    def target_groups(target_name):
        """
        This method returns a list of groups that a target is in.
        """
        groups = []
        for group in Group.objects(): #pylint: disable=no-member
            if target_name in group.member_names:
                groups.append(group.name)

        return list(set(groups))

    @property
    def members(self):
        """
        This property returns member objects of all group members.
        """
        # TODO: Implement membership rules and blacklist
        return Target.objects(name__in=self.whitelist_members) #pylint: disable=no-member

    @property
    def member_names(self):
        """
        This property returns member object names for all group members.
        """
        # TODO: Implement membership rules and blacklist
        return self.whitelist_members
