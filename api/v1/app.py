#!/usr/bin/python3
"""Inicia una app en flask"""

from flask import Flask, render_template
from models import storage
from api.v1.views import app_views
from models.state import State
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def cerrar(self):
    """Elimina la sesión actual de SQLAlchemy"""
    storage.close()


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", default="0.0.0.0")
    port = getenv("HBNB_API_PORT", default="5000")
    app.run(host=host, port=port, threaded=True,  debug=True)
