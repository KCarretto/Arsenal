"""
    This module contains all exceptions thrown by the teamserver,
    as well as a function wrapper that helps ensure that the correct
    responses are returned when an error is encountered.
"""
from functools import wraps
from .models import log
from .config import LOG_LEVEL, LOG_LEVELS

class CannotCancel(Exception):
    """
    This exception is raised when an attempt to cancel an action is made
    but cannot be completed.
    """
    pass

class TargetNotFound(Exception):
    """
    This exception is raised when the referenced target is not found.
    """
    pass

def failed_response(status, description, debug_msg=None):
    """
    A function to generate a failed JSON response.
    """
    if debug_msg is not None and LOG_LEVEL == LOG_LEVELS.get('DEBUG', 0):
        log('DEBUG', '{}|{}'.format(description, debug_msg))
        return {
            'status': status,
            'description': description,
            'debug': debug_msg,
            'error': True,
        }
    return {
        'status': status,
        'description': description,
        'error': True,
    }

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
        except TargetNotFound as exception:
            msg = 'Referenced Target not found.'
            log('INFO', msg)
            return failed_response(404, msg, exception)
        except CannotCancel as exception:
            msg = 'Failed to cancel Action. Action has already been sent'
            log('INFO', msg)
            return failed_response(423, msg, exception)
        except Exception: #pylint: disable=broad-except
            msg = 'Server encountered unhandled exception.'
            return failed_response(500, msg)

    return wrapper
