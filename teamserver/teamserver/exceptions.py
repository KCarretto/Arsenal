"""
    This module contains all exceptions thrown by the teamserver,
    as well as a function wrapper that helps ensure that the correct
    responses are returned when an error is encountered.
"""
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

class CannotRenameTarget(ArsenalException):
    """
    This exception is raised when an attempt to rename a target is made, but a target with
    the new name already exists.
    """
    name = 'cannot-rename-target'

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

class InvalidCredentials(ArsenalException):
    """
    This exception is raised when a user provides invalid credentials.
    """
    name = 'invalid-credentials'

class PermissionDenied(ArsenalException):
    """
    This exception is raised when an authenticated user attempts to perform
    an action that they do not have access to.
    """
    name = 'permission-denied'
