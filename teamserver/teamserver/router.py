"""
This module serves as the entry point for all basic API calls.
It passes appropriate parameter information to various other modules,
that will do the heavy lifting.
"""

from flask import Blueprint, request, jsonify

endpoints = Blueprint('router', __name__)

@endpoints.route("/status")
def teamserver_status():
    """
    This endpoint returns the current status of the teamserver.
    """
    return jsonify(
        {
            'status': 200,
            'state': 'Running',
            'error': False
        }
    )
@endpoints.route("/")
@endpoints.route("/api", methods=["POST"])
@endpoints.route("/api/v1", methods=["POST"])
def api_entry():
    """
    This function serves as the entry point for the v1 JSON API.
    """
    data = request.get_json()
    if data is None:
        data = request.form

