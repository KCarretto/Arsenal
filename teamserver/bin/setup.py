"""
This module will populate the database with default configurations.
"""

import sys

from uuid import uuid4
from os.path import abspath, dirname
from mongoengine import connect
from passlib.hash import bcrypt

sys.path.insert(0, abspath(dirname(abspath(dirname(__file__)))))
from teamserver.models import User, Role, APIKey # pylint: disable-all
from teamserver.config import DB_NAME, DB_HOST, DB_PORT # pylint: disable-all

CONFIG = {
    'users': {
        'admin': str(uuid4()),
        'default-c2': str(uuid4()),
        'guest': str(uuid4()),
    },
    'api_keys': {
        'default-c2': [
            'CreateSession',
            'SessionCheckIn'
        ]
    },
    'roles': {
        'administrator': {
            'users': ['admin'],
            'allowed_api_calls': ['*']
        },
        'logger': {
            'users': [],
            'allowed_api_calls': [
                'CreateLog',
            ]
        },
        'attacker': {
            'users': [],
            'allowed_api_calls': [
                'CreateAction',
                'CreateGroupAction',
            ]
        },
        'spectator': {
            'users': ['guest'],
            'allowed_api_calls': [
                'GetTarget',
                'GetAction',
                'GetSession',
                'GetGroup',
                'GetGroupAction',
                'ListTargets',
                'ListActions',
                'ListSessions',
                'ListGroups',
                'ListGroupActions',
            ]
        },
        'c2': {
            'users': ['default-c2'],
            'allowed_api_calls': [
                'CreateSession',
                'SessionCheckIn',
                'UpdateSessionConfig',
                'SetTargetFacts',
            ]
        }
    }
}

def create_role(name, allowed_api_calls, users):
    """
    Create a role with the given permissions and users.
    """
    role = Role(
        name=name,
        allowed_api_calls=allowed_api_calls,
        users=users,
    )
    role.save()
    return role

def create_user(username, password, administrator=False):
    """
    Create a user with the given password.
    """
    hashed_password = User.hash_password(password)
    user = User(
        username=username,
        password=hashed_password,
        administrator=administrator
    )
    user.save()
    return user

def create_api_key(username, allowed_api_calls):
    """
    Create an API key for a user with the given permissions.
    """
    key = APIKey(
        key='{}{}{}{}{}'.format(
            str(uuid4()),
            str(uuid4()),
            str(uuid4()),
            str(uuid4()),
            str(uuid4()),
            ),
        owner=username,
        allowed_api_calls=allowed_api_calls
    )
    key.save()
    return key

def main():
    """
    The main entry point of the program.
    """
    connect(DB_NAME, host=DB_HOST, port=DB_PORT)


    print('Generating authentication schema...')
    for username, password in CONFIG['users'].items():
        user = create_user(username, password, username=='admin')
        print('[+][Created User] {}:{}'.format(user.username, password))
    print('')
    for rolename, roleconfig in CONFIG['roles'].items():
        role = create_role(rolename, roleconfig['allowed_api_calls'], roleconfig['users'])
        print('[+][Created Role] {}:{}:{}'.format(
            rolename,
            ','.join(role.users),
            ','.join(role.allowed_api_calls)))
    print('')
    for owner, allowed_api_calls in CONFIG['api_keys'].items():
        api_key = create_api_key(owner, allowed_api_calls)
        print('[+][Created API Key] {}:{}:{}'.format(
            api_key.key,
            api_key.owner,
            ','.join(api_key.allowed_api_calls)))
    print('')

if __name__ == '__main__':
    main()
