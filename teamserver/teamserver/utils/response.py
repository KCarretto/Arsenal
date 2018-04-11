"""
This module includes functionality that can be used to build responses to return to the user.
"""
import gzip
import functools

from cStringIO import StringIO as IO
from flask import jsonify, after_this_request, request

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

def gzipped(func):
    """
    Function wrapper that will return a gzip encoded response.

    Thanks to http://flask.pocoo.org/snippets/122/
    """
    @functools.wraps(func)
    def view_func(*args, **kwargs):
        @after_this_request
        def zipper(response): # pylint: disable-all
            accept_encoding = request.headers.get('Accept-Encoding', '')

            if 'gzip' not in accept_encoding.lower():
                return response

            response.direct_passthrough = False

            if (
                    response.status_code < 200 or
                    response.status_code >= 300 or
                    'Content-Encoding' in response.headers
                ):
                return response
            gzip_buffer = IO()
            gzip_file = gzip.GzipFile(
                mode='wb',
                fileobj=gzip_buffer)
            gzip_file.write(response.data)
            gzip_file.close()

            response.data = gzip_buffer.getvalue()
            response.headers['Content-Encoding'] = 'gzip'
            response.headers['Vary'] = 'Accept-Encoding'
            response.headers['Content-Length'] = len(response.data)

            return response

        return func(*args, **kwargs)

    return view_func
