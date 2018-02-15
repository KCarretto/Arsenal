"""
This module serves as the entry point for all basic API calls.
It passes appropriate parameter information to various other modules,
that will do the heavy lifting.
"""

from flask import Blueprint,request, jsonify

endpoints = Blueprint('router', __name__)

@endpoints.route("/status")
def teamserver_status():
    return jsonify(
            {
                'status': 200,
                'state': 'Running',
                'error': False
            }
        )

