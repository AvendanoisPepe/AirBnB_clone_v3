#!/usr/bin/python3
"""Indexhtml."""
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from models import storage


@app_views.route("/status", strict_slashes=False)
def hbnbStatus():
    """def hbnbStatus"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stat():
    """retrieves the number of each objects"""
    dic = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return(jsonify(dic))
