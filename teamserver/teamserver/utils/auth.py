"""
This module is used to determine if a request is properly authenticated.
"""
from mongoengine import DoesNotExist
from ..models import User, APIKey
from ..exceptions import InvalidCredentials, PermissionMismatch

def _get_user(params):
    """
    Returns a user object based on the arsenal_auth_object.
    """
    # Retrieve current authentication context
    auth_obj = params['arsenal_auth_object']

    # Lookup user object if authentication object was an API key
    user = params['arsenal_auth_object']
    if isinstance(auth_obj, APIKey):
        user = User.get_user(auth_obj.owner)

        # Ensure API Key has subset of User permissions
        if any([method not in user.allowed_api_calls for method in auth_obj.allowed_api_calls]):
            raise PermissionMismatch('API Key has more privileges than user.')

    # Return allowed_api_calls to prevent API keys from assuming user permissions
    return (user, auth_obj.allowed_api_calls)

def get_context(params):
    """
    Allow administrative users to assume another user context.
    """
    user, allowed_methods = _get_user(params)
    administrator = user.administrator
    # Allow administrators to override the owner with a custom value
    if params.get('user_context') and administrator:
        # Change the operating user context
        user = User.get_user(params['user_context'])
        allowed_methods = user.allowed_api_calls

    return (user, allowed_methods, administrator)

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
    api_key = data.get('login_api_key')
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
    username = data.get('login_username')
    password = data.get('login_password')

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
                'error_type': 'invalid-user',
                'error': True
            })
        except InvalidCredentials:
            return (False, {
                'status': 403,
                'description': 'Invalid Credentials.',
                'error_type': 'invalid-credentials',
                'error': True
            })

    # If no authentication options were specified
    return (False, {
        'status': 401,
        'description': 'Unauthorized. Please authenticate.',
        'error': True
    })
