#!/usr/bin/python3
"""Inicia una app en flask"""

from api.v1.views import app_views
from models import storage
from models.state import State
from os import getenv
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ estatus cuo xd """
    return jsonify({"status": "OK"})
