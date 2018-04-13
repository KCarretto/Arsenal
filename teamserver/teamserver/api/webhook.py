"""
    This module contains all 'Webhook' API functions.
"""
from uuid import uuid4

from ..utils import success_response, handle_exceptions, get_context
from ..exceptions import PermissionDenied
from ..models import Webhook

@handle_exceptions
def register_webhook(params):
    """
    ### Overview
    This API function will register a new webhook.

    ### Parameters
    post_url (required):        The url that the data should be sent via JSON in a POST request.
                                    <str>
    event_triggers (required):  A list of events to subscribe to. <str>
    """
    user, _, _ = get_context(params)

    hook = Webhook(
        hook_id=str(uuid4()),
        owner=user.username,
        post_url=params['post_url'],
        event_triggers=params['event_triggers'],
    )
    hook.save()

    return success_response(hook_id=hook.hook_id)

@handle_exceptions
def unregister_webhook(params):
    """
    ### Overview
    This API function will unregister a webhook.

    ### Parameters
    hook_id (required): The identifier of the hook to unregister.
    """
    user, _, administrator = get_context(params)

    webhook = Webhook.get_hook(params['hook_id'])

    if webhook.owner != user.username and not administrator:
        raise PermissionDenied('Cannot delete a webhook that you do not own.')

    webhook.remove()

    return success_response()

@handle_exceptions
def list_webhooks(params): #pylint: disable=unused-argument
    """
    ### Overview
    This API function will return a list of a user's webhooks.

    ### Parameters
    user_context (optional, requires administrator) <str>
    """
    user, _, _ = get_context(params)

    return success_response(hooks=[
        hook.document for hook in Webhook.list_hooks(user.username)])
