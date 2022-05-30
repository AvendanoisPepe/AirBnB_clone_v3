#!/usr/bin/python3
"""Connect"""
import os
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, make_response
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_base(self):
    """def close"""
    storage.close()


@app.errorhandler(404)
def error_handler(error):
    """error 404"""
    return(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host=os.getenv("HBNB_API_HOST", "0.0.0.0"),
            port=int(os.getenv("HBNB_API_PORT", "5000")))
