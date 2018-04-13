"""
    This module contains all 'Log' API functions.
"""
from ..utils import success_response, handle_exceptions, log
from ..models import Log

@handle_exceptions
def create_log(params):
    """
    ### Overview
    Log an entry (if current log level deems necessary)

    ### Parameters
    application:    The application that is requesting to log a message. <str>
    level:          The log level that the message is at (LOG_LEVELS in config.py). <str>
    message:        The message to log. <str>
    """
    log(params['level'], params['message'], params['application'])
    return success_response()

@handle_exceptions
def list_logs(params):
    """
    ### Overview
    Show filtered log entries

    ### Parameters
    application (optional):         The application to filter for. <str>
    since (optional):               The timestamp that logs must be newer than. <float>
    include_archived (optional):    Should archived messages be included. Default: False. <bool>
    levels (optional):              The level to filter for. <list[str]>
    """
    logs = Log.list_logs(
        params.get('include_archived', False),
        params.get('application'),
        params.get('since', 0),
        params.get('levels'))

    return success_response(logs=[entry.document for entry in logs])
