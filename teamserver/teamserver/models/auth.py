"""
    This module defines a python object model for the Role and User document
    in the backend MongoDB database.

    Users have API Keys
    API keys have Roles
    Roles have permissions
"""
from mongoengine import Document
from mongoengine.fields import ListField, StringField
from passlib.hash import bcrypt
from ..exceptions import InvalidCredentials, PermissionDenied
from ..config import MAX_STR_LEN, COLLECTION_USERS, COLLECTION_ROLES, COLLECTION_APIKEYS

class Role(Document):
    """
    This class represents a role, which consists of a list of API calls that are permitted.
    """
    meta = {
        'collection': COLLECTION_ROLES,
        'indexes': [
            {
                'fields': ['name'],
                'unique': True
            }
        ]
    }
    name = StringField(required=True, null=False, unique=True, max_length=MAX_STR_LEN)
    allowed_api_calls = ListField(
        StringField(required=True, null=False, max_length=MAX_STR_LEN),
        required=True,
        null=False)
    users = ListField(
        StringField(required=True, null=False, max_length=MAX_STR_LEN),
        required=True)

class APIKey(Document):
    """
    This class represents an API key.
    It has it's own unique set of permissions, and an owner.
    """
    meta = {
        'collection': COLLECTION_APIKEYS,
        'indexes': [
            {
                'fields': ['key'],
                'unique': True
            }
        ]
    }
    key = StringField(
        primary_key=True,
        required=True,
        null=False,
        unique=True,
        max_length=MAX_STR_LEN)
    owner = StringField(required=True, null=False, max_length=MAX_STR_LEN)
    allowed_api_calls = ListField(
        StringField(required=True, null=False, max_length=MAX_STR_LEN),
        required=True,
        null=False)

    @staticmethod
    def get_key(key):
        """
        Query for a key from the database.
        """
        return APIKey.objects().get(key=key) # pylint: disable=no-member

    def is_permitted(self, api_method):
        """
        Determines if the API key has permissions to execute an API method.
        """
        if api_method in self.allowed_api_calls: # pylint: disable=unsupported-membership-test
            return True
        raise PermissionDenied('API Key does not have access to this method.')

class User(Document):
    """
    This class represents a User.
    It defines user settings and permissions.
    """
    meta = {
        'collection': COLLECTION_USERS,
        'indexes': [
            {
                'fields': ['username'],
                'unique': True
            }
        ]
    }
    username = StringField(required=True, null=False, unique=True, max_length=MAX_STR_LEN)
    password = StringField(required=True, null=False, unique=True, max_length=MAX_STR_LEN)

    @staticmethod
    def get_user(username):
        """
        Query for a user by username.
        """
        return User.objects().get(username=username) # pylint: disable=no-member

    @property
    def api_keys(self):
        """
        Return a list of all API keys that belong to this user.
        """
        return APIKey.objects(owner=self.username) # pylint: disable=no-member

    @property
    def document(self):
        """
        This property filters and returns the JSON information for a queried agent.
        """
        return {
            'username': self.username,
            'roles': self.roles,
        }

    @property
    def roles(self):
        """
        Return all roles that this user is in.
        """
        return Role.objects(users=self.username) # pylint: disable=no-member

    def is_permitted(self, api_method):
        """
        Determines if a user is allowed to execute an API call based on the given roles.
        """
        for role in self.roles:
            if api_method in role.allowed_api_calls:
                return True
        raise PermissionDenied('Permission denied.')

    def authenticate(self, password):
        """
        Determines if a user is authenticated given a password.
        Raises an InvalidCredentials exception if the password was incorrect.
        """
        if not bcrypt.verify(password, self.password):
            raise InvalidCredentials('Password incorrect.')
        return True

    def update_password(self, current_password, new_password):
        """
        Updates a user's password.
        """
        if self.authenticate(current_password):
            self.password = bcrypt.hash(new_password)
            self.save()

    def remove(self):
        """
        Remove this document from the database, and perform any related cleanup.
        """
        self.delete()
