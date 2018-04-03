"""
This module is used to determine if a request is properly authenticated.
"""
from mongoengine import DoesNotExist
from .models import User, APIKey
from .exceptions import InvalidCredentials

def authenticate(request):
    """
    Determine if a request is authenticated.

    Returns (True, AuthToken) or (False, Error)
    """
    # Fetch data from request
    data = request.get_json()
    if data is None:
        data = request.form

    # Check for a session_token
    session_token = request.cookies.get('session_token')

    # TODO: Validate session token
    if session_token:
        pass

    # Attempt to get an api_key from parameters
    api_key = data.get('api_key')
    if not api_key:
        # Attempt to get from headers
        api_key = request.headers.get('X-Arsenal-API-Key')

    # Validate api key
    if api_key:
        try:
            key = APIKey.get_key(api_key)
            return (True, key)
        except DoesNotExist:
            return (False, {
                'status': 403,
                'description': 'Invalid API Key.',
                'error': True
            })

    # Attempt user based authentication
    username = data.get('username')
    password = data.get('password')

    # Validate user
    if username and password:
        try:
            user = User.get_user(username)
            if user.authenticate(password):
                return (True, user)
        except DoesNotExist:
            return (False, {
                'status': 403,
                'description': 'Invalid User.',
                'error': True
            })
        except InvalidCredentials:
            return (False, {
                'status': 403,
                'description': 'Invalid Credentials.',
                'error': True
            })

    # If no authentication options were specified
    return (False, {
        'status': 401,
        'description': 'Unauthorized. Please authenticate.',
        'error': True
    })
