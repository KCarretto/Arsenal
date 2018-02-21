"""
    This module contains all exceptions thrown by the teamserver,
    as well as a function wrapper that helps ensure that the correct
    responses are returned when an error is encountered.
"""
from functools import wraps

def handle_exceptions(func):
    """
    This function can be used as a decorator to wrap functions.
    Wrapped functions will be surrounded in a try / except block that
    includes necessary error handling, including logging and
    returning error responses.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        This uses the func tools library to wrap a function.
        """

        try:
            retval = func(*args, **kwargs)
            return retval
        except Exception: # TODO: as e:
            return {
                'status': 503,
                'description': 'Server encountered unhandled exception.',
                # TODO: Include exception message if debug mode enabled
                'error': True
            }

    return wrapper
