"""
    This module contains all 'Auth' API functions.
"""
from uuid import uuid4

from base64 import b64encode
from argon2 import argon2_hash

from ..utils import handle_exceptions, success_response, get_context
from ..exceptions import PermissionDenied
from ..models import User, APIKey, Role
from ..config import API_KEY_SALT, HASH_TIME_PARAM, HASH_MEMORY_PARAM, HASH_PARALLELIZATION_PARAM

@handle_exceptions
def create_user(params):
    """
    Create a user.

    username (required, unique): The username of the user.
    password (required): The desired password for the user.
    """

    password_hash = User.hash_password(params['password'])
    del params['password']

    user = User(
        username=params['username'],
        password=password_hash,
        administrator=False
    )
    user.save(force_insert=True)

    return success_response()

@handle_exceptions
def create_api_key(params):
    """
    Create an API key for a user.

    allowed_api_calls (optional): A list of API calls that the API token can perform. If left
                                  empty, all of the user's permissions will be granted to the
                                  token. This may not specify any API call that the user does not
                                  currently have access to. <list>

    user_context (optional, requires administrator)
    """
    # Retrieve the current user object (Allowing for administrator overrides)
    user, allowed_methods, _ = get_context(params)

    # Set the owner of the new API key to be the current user
    owner = user.username

    allowed_api_calls = params.get('allowed_api_calls')

    # Verify allowed api calls
    if allowed_api_calls:
        if any(method not in allowed_methods for method in allowed_api_calls):
            if '*' not in allowed_methods:
                raise PermissionDenied(
                    'Cannot create API key with more permissions than key owner.')
    else:
        allowed_api_calls = allowed_methods

    # Create the key
    original_key = '{}{}{}{}{}'.format(
        str(uuid4()),
        str(uuid4()),
        str(uuid4()),
        str(uuid4()),
        str(uuid4()),
        )
    mid_hash = b64encode(argon2_hash(password=original_key,
                                     salt=API_KEY_SALT,
                                     t=HASH_TIME_PARAM,
                                     m=HASH_MEMORY_PARAM,
                                     p=HASH_PARALLELIZATION_PARAM)).decode()

    key = APIKey(
        key=API_KEY_SALT + "$" + mid_hash,
        owner=owner,
        allowed_api_calls=allowed_api_calls
    )
    key.save(force_insert=True)

    return success_response(api_key=original_key)

@handle_exceptions
def create_role(params):
    """
    Create a role.

    name (required, unique): The name of the role.
    allowed_api_calls (required): The list of API methods that users with this role may invoke.

    users (optional): Specify a list of users to add to the role.
    """
    # Get role parameters
    name = params['name']
    allowed_api_calls = params['allowed_api_calls']
    users = []
    if params.get(users):
        users = [User.get_user(user).username for user in params['users']]

    # Create the role
    role = Role(
        name=name,
        allowed_api_calls=allowed_api_calls,
        users=users
    )
    role.save(force_insert=True)

    return success_response()

@handle_exceptions
def update_user_password(params):
    """
    Changes a users password. Requires the user's current password.

    current_password (required): The user's current password.
    new_password (required): The user's new password.

    user_context (optional, requires administrator): An administrator may specify which user
                                                    password to change.
    """
    user, _, administrator = get_context(params)

    # Allow administrator to change (non-admin user) password without current
    if administrator and not user.administrator:
        user.password = User.hash_password(params['new_password'])
        user.save()
        return success_response()

    user.update_password(params['current_password'], params['new_password'])

    return success_response()

@handle_exceptions
def update_role_permissions(params):
    """
    Update the permission set of a role.

    role_name (required): The name of the role to update.
    allowed_api_calls (required): The new list of allowed api methods.
    """
    role = Role.get_role(params['role_name'])
    role.allowed_api_calls = params['allowed_api_calls']
    role.save()

    return success_response()

@handle_exceptions
def add_role_member(params):
    """
    Add a user to a role.

    role_name (required): The name of the role to modify.
    username (required): The name of the user to add.
    """
    role = Role.get_role(params['role_name'])
    role.add_member(params['username'])

    return success_response()

@handle_exceptions
def remove_role_member(params):
    """
    Remove a user from a role.

    role_name (required): The name of the role to modify.
    username (required): The name of the user to remove.
    """
    role = Role.get_role(params['role_name'])
    role.remove_member(params['username'])

    return success_response()

@handle_exceptions
def get_user(params):
    """
    Retrieve a user object.

    username (required): The name of the user object to fetch. <str>
    include_roles (optional): Optionally include roles.
                                    default: False. <bool>
    include_api_calls (optional): Display the set of permitted API calls for the user.
                                    default: True. <bool>
    """
    user = User.get_user(params['username'])

    return success_response(
        user=user.document(
            params.get('include_roles', False),
            params.get('include_api_calls', False)
        ))

@handle_exceptions
def get_role(params):
    """
    Retrieve a role object.

    role_name (required): The name of the role to fetch. <str>
    """
    role = Role.get_role(params['role_name'])

    return success_response(role=role.document)

@handle_exceptions
def get_current_context(params):
    """
    Return the currently authenticated username.
    """
    user, allowed_methods, _ = get_context(params)
    return success_response(
        user={
            'username': user.username,
            'allowed_api_calls': allowed_methods
        }
    )

@handle_exceptions
def list_users(params):
    """
    Return a list of users.

    include_roles (optional): Optionally include roles.
                                    default: False. <bool>
    include_api_calls (optional): Display the set of permitted API calls for the user.
                                    default: True. <bool>
    """

    return success_response(users=[user.document(
        params.get('include_roles'),
        params.get('include_api_calls'),
    ) for user in User.list_users()])

@handle_exceptions
def list_api_keys(params):
    """
    Lists the permissions of API keys that you own. This will not return the API key itself.

    user_context (optional, requires administrator)
    """
    user, _, _ = get_context(params)

    return success_response(api_keys=[key.document for key in APIKey.list_keys(user.username)])

@handle_exceptions
def list_roles(params): #pylint: disable=unused-argument
    """
    Return a list of roles.
    """
    return success_response(roles=[role.document for role in Role.list_roles()])

@handle_exceptions
def delete_user(params):
    """
    Delete a user.

    username (required): The name of the user to delete. <str>
    """
    user = User.get_user(params['username'])

    user.remove()

    return success_response()

@handle_exceptions
def delete_role(params):
    """
    Delete a role.

    role_name(required): The name of the role to delete.
    """
    role = Role.get_role(params['role_name'])

    role.remove()

    return success_response()

@handle_exceptions
def revoke_api_key(params):
    """
    Revoke a user's API key.

    api_key (required): The API key to revoke.

    user_context (optional, requires administrator)
    """
    user, _, administrator = get_context(params)

    api_key = APIKey.get_key(params['api_key'])

    if api_key.owner != user.username and not administrator:
        raise PermissionDenied('Cannot revoke an API key you do not own.\
        Please authenticate as the owner of the key to revoke it.')

    api_key.remove()

    return success_response()
