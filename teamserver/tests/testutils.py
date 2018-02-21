"""
    This module provides general utillities accessed by test cases.
"""
import sys
import os

# Configure path to include teamserver module
sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))

import teamserver #pylint: disable=wrong-import-position

def create_test_app():
    """
    This function creates the flask application with test values.
    """
    return teamserver.create_app(
        TESTING=True,
        MONGODB_SETTINGS=
        {
            'db': 'arsenal_default',
            'host': 'mongomock://localhost',
            'is_mock': True
        })
