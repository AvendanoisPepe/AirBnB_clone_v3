#!/usr/bin/python3
"""Inicia una app en flask"""

from flask import Flask, render_template, Blueprint, jsonify, make_response
from models import storage
from api.v1.views import app_views
from models.state import State
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def cerrar(self):
    """Elimina la sesión actual de SQLAlchemy"""
    storage.close()


@app.errorhandler(404)
def error_handler(error):
    """No found 404"""
    return(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", default="0.0.0.0")
    port = getenv("HBNB_API_PORT", default="5000")
    app.run(host=host, port=port, threaded=True,  debug=True)
