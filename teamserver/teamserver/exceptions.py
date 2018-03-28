"""
    This module contains all exceptions thrown by the teamserver,
    as well as a function wrapper that helps ensure that the correct
    responses are returned when an error is encountered.
"""
from functools import wraps
from mongoengine.errors import DoesNotExist, NotUniqueError, ValidationError
from .models import log
from .config import LOG_LEVEL

class CannotCancel(Exception):
    """
    This exception is raised when an attempt to cancel an action is made
    but cannot be completed.
    """
    pass

class UnboundException(Exception):
    """
    This exception is raised when the Session that an Action was assigned to no longer exists.
    """
    pass

class CannotAssign(Exception):
    """
    This exception is raised when an Action is unable to be assigned to the given session_id.
    """
    pass

class NoTarget(Exception):
    """
    This exception is raised when an Action is attempted to be assigned to a
    Target that does not exist.
    """
    pass

class ActionParseException(Exception):
    """
    This exception is raised when an error was encountered while parsing an action string.
    """
    pass

class MembershipException(Exception):
    """
    This exception is raised when an attempt to modify group membership is made
    and cannot be completed.
    """
    pass

def failed_response(status, description, log_msg=None, log_level=None):
    """
    A function to generate a failed JSON response. If the LOG_LEVEL 'DEBUG' is set,
    log messages will be included in the JSON response.

    status: The status code to return.
    description: A description of the error code to return.
    log_msg: A log message to raise, default to DEBUG log level.
    log_level: The level to raise the log message to.
    """

    if log_msg is not None and log_level is not None:
        log(log_level, '{}|{}'.format(description, str(log_msg)))

        if LOG_LEVEL == 'DEBUG':
            return {
                'status': status,
                'description': description,
                'debug': str(log_msg),
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
    def wrapper(*args, **kwargs): #pylint: disable=too-many-return-statements
        """
        This uses the func tools library to wrap a function.
        """
        try:
            retval = func(*args, **kwargs)
            return retval

        # Arsenal Specific Exceptions
        except CannotCancel as exception:
            msg = 'Failed to cancel Action. Action has already been sent.'
            return failed_response(423, msg, exception)

        except NoTarget as exception:
            msg = 'Failed to create Action. No such Target.'
            return failed_response(404, msg, exception)

        except ActionParseException as exception:
            msg = 'Invalid action syntax.'
            return failed_response(400, msg, exception)

        except MembershipException as exception:
            return failed_response(400, exception)

        # Mongoengine Exceptions
        except ValidationError as exception:
            msg = 'Invalid field type.'
            return failed_response(400, msg, exception)

        except DoesNotExist as exception:
            msg = 'Resource not found.'
            return failed_response(404, msg, exception)

        except NotUniqueError as exception:
            msg = 'Resource already exists.'
            return failed_response(422, msg, exception)

        # Python Exceptions
        except KeyError as exception:
            msg = 'Missing required parameter.'
            return failed_response(422, msg, exception)

        except Exception as exception: #pylint: disable=broad-except
            msg = 'Server encountered unhandled exception.'
            return failed_response(500, msg, exception, 'CRIT')

    return wrapper
