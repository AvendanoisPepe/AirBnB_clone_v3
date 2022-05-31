#!/usr/bin/python3
"""New Amenity"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage


@app_views.route("/amenities", strict_slashes=False, methods=['GET'])
def get_all_amenities():
    """def get"""
    return jsonify([amenity.to_dict() for amenity in
                    storage.all(Amenity).values()]), 200


@app_views.route("/amenities/<amenity_id>",
                 methods=['GET'], strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """return amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict()), 200


@app_views.route("/amenities/<amenity_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", strict_slashes=False, methods=['POST'])
def create_amenity():
    """returns a new amenity"""
    amenity_json = request.get_json(silent=True)
    if not amenity_json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in amenity_json:
        return jsonify({"error": "Missing name"}), 400
    amenity = Amenity(**amenity_json)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """information of amenity"""
    keys = ['id', 'created_at', 'updated_at']
    amenity_json = request.get_json(silent=True)

    if not amenity_json:
        return jsonify({"error": "Not a JSON"}), 400
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    for count, val in amenity_json.items():
        if count not in keys:
            setattr(amenity, count, val)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
