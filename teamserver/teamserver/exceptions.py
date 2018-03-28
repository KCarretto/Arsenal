"""
    This module contains all exceptions thrown by the teamserver,
    as well as a function wrapper that helps ensure that the correct
    responses are returned when an error is encountered.
"""
from functools import wraps
from mongoengine.errors import DoesNotExist, NotUniqueError, ValidationError
from .models import log
from .config import LOG_LEVEL

class ArsenalException(Exception):
    """
    A base class for Arsenal Exceptions.
    """
    name = 'arsenal-exception'

class ActionUnboundSession(ArsenalException):
    """
    This exception is raised when the Session that an Action was assigned to no longer exists.
    """
    name = 'action-unbound-session'

class SessionUnboundTarget(ArsenalException):
    """
    This exception is raised when a Session's Target does not exist.
    """
    name = 'session-unbound-target'

class CannotCancelAction(ArsenalException):
    """
    This exception is raised when an attempt to cancel an action is made
    but cannot be completed.
    """
    name = 'cannot-cancel-action'

class CannotAssignAction(ArsenalException):
    """
    This exception is raised when an Action is unable to be assigned to the given session_id.
    """
    name = 'cannot-assign-action'

class CannotBindAction(ArsenalException):
    """
    This exception is raised when an Action is attempted to be assigned to a
    Target that does not exist.
    """
    name = 'cannot-bind-action'

class ActionSyntaxError(ArsenalException):
    """
    This exception is raised when an error was encountered while parsing an action string.
    """
    name = 'action-syntax-error'

class MembershipError(ArsenalException):
    """
    This exception is raised when an attempt to modify group membership is made
    and cannot be completed.
    """
    name = 'membership-error'

def failed_response(status, description, error_type, log_msg=None, log_level=None):
    """
    A function to generate a failed JSON response. If the LOG_LEVEL 'DEBUG' is set,
    log messages will be included in the JSON response.

    status: The status code to return.
    description: A description of the error code to return.
    exception: The exception that was raised.
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
                'error_type': error_type,
                'error': True,
            }
    return {
        'status': status,
        'description': description,
        'error_type': error_type,
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

        # Arsenal Exceptions
        except ActionUnboundSession as exception:
            msg = 'Action no longer can find assigned Session.'
            return failed_response(500, msg, exception.name, exception, 'WARN')
        except SessionUnboundTarget as exception:
            msg = 'Session no longer can find assigned Target.'
            return failed_response(500, msg, exception.name, exception, 'WARN')
        except CannotCancelAction as exception:
            msg = 'Cannot cancel Action.'
            return failed_response(400, msg, exception.name)
        except CannotAssignAction as exception:
            msg = 'Action cannot be assigned to Session because it is bound.'
            return failed_response(400, msg, exception.name)
        except CannotBindAction as exception:
            msg = 'Target for Action does not exist.'
            return failed_response(400, msg, exception.name)
        except ActionSyntaxError as exception:
            msg = 'Invalid Action Syntax.'
            return failed_response(400, msg, exception.name)
        except MembershipError as exception:
            msg = 'Invalid membership modification request.'
            return failed_response(400, msg, exception.name)

        # Mongoengine Exceptions
        except ValidationError as exception:
            msg = 'Invalid field type.'
            return failed_response(400, msg, 'validation-error')

        except DoesNotExist as exception:
            msg = 'Resource not found.'
            return failed_response(404, msg, 'resource-not-found')

        except NotUniqueError as exception:
            msg = 'Resource already exists.'
            return failed_response(422, msg, 'resource-already-exists')

        # Python Exceptions
        except KeyError as exception:
            msg = 'Missing required parameter.'
            return failed_response(400, msg, 'missing-parameter')

        # Broad Except for all other cases
        except Exception as exception: #pylint: disable=broad-except
            msg = 'Server encountered unhandled exception.'
            print(exception)
            return failed_response(500, msg, 'unhandled-exception', exception, 'CRIT')

    return wrapper
