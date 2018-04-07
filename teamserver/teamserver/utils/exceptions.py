"""
This module provides additional exception handling functionality.
"""
from functools import wraps
from mongoengine.errors import DoesNotExist, NotUniqueError, ValidationError

from .response import failed_response

from ..exceptions import ActionUnboundSession, SessionUnboundTarget
from ..exceptions import CannotCancelAction, CannotAssignAction, CannotBindAction
from ..exceptions import CannotRenameTarget, MembershipError
from ..exceptions import InvalidCredentials, PermissionDenied, ActionSyntaxError

def handle_exceptions(func):
    """
    This function can be used as a decorator to wrap functions.
    Wrapped functions will be surrounded in a try / except block that
    includes necessary error handling, including logging and
    returning error responses.
    """

    @wraps(func)
    def wrapper(*args, **kwargs): #pylint: disable=too-many-return-statements,too-many-branches
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
        except CannotRenameTarget as exception:
            msg = 'Target with new name already exists.'
            return failed_response(400, msg, exception.name)
        except ActionSyntaxError as exception:
            msg = 'Invalid Action Syntax.'
            return failed_response(400, msg, exception.name)
        except MembershipError as exception:
            msg = 'Invalid membership modification request.'
            return failed_response(400, msg, exception.name)
        except InvalidCredentials as exception:
            msg = 'Provided credentials are invalid.'
            return failed_response(403, msg, exception.name)
        except PermissionDenied as exception:
            msg = 'Permission to access method was denied.'
            return failed_response(401, msg, exception.name)

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
