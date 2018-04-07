"""
This module includes functionality that can be used to build responses to return to the user.
"""
from flask import jsonify
from ..config import LOG_LEVEL

def respond(response):
    """
    This method will return a jsonfied response, with the correct http headers.
    """
    resp = jsonify(response)
    resp.status_code = response.get('status', 500)
    return resp

def success_response(**kwargs):
    """
    This function will generate a dictionary with generic successful
    response keys, as well as any key value pairs provided.
    """
    response = {}

    for key, value in kwargs.items():
        response[key] = value

    response['status'] = 200
    response['error'] = False

    return response

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
        #log(log_level, '{}|{}'.format(description, str(log_msg)))

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
