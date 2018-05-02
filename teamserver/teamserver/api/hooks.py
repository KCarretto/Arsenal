"""
This module contains various hooks from database mutations.
"""
import time

from uuid import uuid4

def in_create_session(**kwargs):
    """
    This function defines an input hook for create_session.

    This allows us to automatically generate the session_id, and set the proper timestamp.
    """
    kwargs['session_id'] = str(uuid4())
    kwargs['timestamp'] = time.time()
    return kwargs
