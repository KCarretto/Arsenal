"""
    This module defines a python object model for the Role and User document
    in the backend MongoDB database.

    Users have API Keys
    API keys have Roles
    Roles have permissions
"""
from mongoengine import Document
from mongoengine.fields import ListField, StringField, BooleanField
import bcrypt
from ..exceptions import InvalidCredentials #, PermissionDenied
from ..config import MAX_STR_LEN, MAX_BIGSTR_LEN, API_KEY_SALT
from ..config import COLLECTION_USERS, COLLECTION_ROLES, COLLECTION_APIKEYS

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
    description = StringField(required=False, max_length=MAX_BIGSTR_LEN)
    allowed_api_calls = ListField(
        StringField(required=True, null=False, max_length=MAX_STR_LEN),
        required=True,
        null=False)
    users = ListField(StringField(required=True, null=False, max_length=MAX_STR_LEN))

    @staticmethod
    def list_roles():
        """
        Return a list of role objects.
        """
        return Role.objects() # pylint: disable=no-member

    @staticmethod
    def get_role(role_name):
        """
        Fetch a role by name.
        """
        return Role.objects.get(name=role_name) # pylint: disable=no-member

    @property
    def document(self):
        """
        This property filters and returns the JSON information for a queried role.
        """
        return {
            'name': self.name,
            'description': self.description,
            'allowed_api_calls': self.allowed_api_calls,
            'users': self.users,
        }

    def add_member(self, username):
        """
        Add a user to this role if it exists.
        """
        user = User.get_user(username)
        if user.username not in self.users: #pylint: disable=unsupported-membership-test
            self.users.append(user.username) # pylint: disable=no-member
            self.save()
        # TODO: Raise exception

    def remove_member(self, username):
        """
        Remove a user from this role.
        """
        if username in self.users: #pylint: disable=unsupported-membership-test
            self.users.remove(username) #pylint: disable=no-member
            self.save()
        # TODO: Raise exception if user not in list

    def remove(self):
        """
        Remove this document from the database, and perform any related cleanup.
        """
        self.delete()

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
        required=True,
        null=False,
        unique=True,
        max_length=MAX_BIGSTR_LEN)
    owner = StringField(required=True, null=False, max_length=MAX_STR_LEN)
    allowed_api_calls = ListField(
        StringField(required=True, null=False, max_length=MAX_STR_LEN),
        required=True,
        null=False)

    @staticmethod
    def list_keys(owner):
        """
        List the keys for a user.
        """
        return APIKey.objects(owner=owner) # pylint: disable=no-member

    @staticmethod
    def get_key(key):
        """
        Query for a key from the database.
        """
        return APIKey.objects.get(key=bcrypt.hashpw(key, API_KEY_SALT)) # pylint: disable=no-member

    @property
    def document(self):
        """
        Returns a document for this object. Does not include the API key itself.
        """
        return {
            'owner': self.owner,
            'allowed_api_calls': self.allowed_api_calls,
        }

    def is_permitted(self, api_method):
        """
        Determines if the API key has permissions to execute an API method.
        """
        if api_method in self.allowed_api_calls: # pylint: disable=unsupported-membership-test
            return True
        if '*' in self.allowed_api_calls: # pylint: disable=unsupported-membership-test
            return True
        return False

    def remove(self):
        """
        Remove this document from the database, and perform any related cleanup.
        """
        self.delete()

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
    administrator = BooleanField(required=True, null=False, default=False)

    @staticmethod
    def list_users():
        """
        Return a list of user objects.
        """
        return User.objects() # pylint: disable=no-member

    @staticmethod
    def get_user(username):
        """
        Query for a user by username.
        """
        return User.objects.get(username=username) # pylint: disable=no-member

    @property
    def api_keys(self):
        """
        Return a list of all API keys that belong to this user.
        """
        return APIKey.objects(owner=self.username) # pylint: disable=no-member

    def document(self, include_roles=False, include_api_calls=True):
        """
        This property filters and returns the JSON information for a queried user.
        """
        resp = {
            'username': self.username,
        }
        if include_roles:
            resp['roles'] = [role.document for role in self.roles]
        if include_api_calls:
            resp['allowed_api_calls'] = self.allowed_api_calls

        return resp

    @property
    def roles(self):
        """
        Return all roles that this user is in.
        """
        return Role.objects(users=self.username) # pylint: disable=no-member

    @staticmethod
    def hash_password(password):
        """
        Returns a hash of a password.
        """
        return bcrypt.hashpw(password, bcrypt.gensalt())

    @property
    def allowed_api_calls(self):
        """
        Return a list of all API methods this user may execute.
        """
        allowed_methods = []
        for role in self.roles:
            allowed_methods += role.allowed_api_calls
        return list(set(allowed_methods))

    def is_permitted(self, api_method):
        """
        Determines if a user is allowed to execute an API call based on the given roles.
        """
        if self.administrator:
            return True

        allowed_methods = self.allowed_api_calls
        if isinstance(allowed_methods, list) and '*' in allowed_methods:
            return True
        if isinstance(allowed_methods, list) and api_method in allowed_methods:
            return True
        return False

    def authenticate(self, password):
        """
        Determines if a user is authenticated given a password.
        Raises an InvalidCredentials exception if the password was incorrect.
        """
        if not bcrypt.checkpw(password, self.password):
            raise InvalidCredentials('Password incorrect.')
        return True

    def update_password(self, current_password, new_password):
        """
        Updates a user's password.
        """
        if self.authenticate(current_password):
            self.password = self.hash_password(new_password)
            self.save()
        return True

    def remove(self):
        """
        Remove this document from the database, and perform any related cleanup.
        """
        for api_key in self.api_keys:
            api_key.remove()
        self.delete()
