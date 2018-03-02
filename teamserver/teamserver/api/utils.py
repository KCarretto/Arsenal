"""
    This module provides utillity functions accessible by all API modules.
"""

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
