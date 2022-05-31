#!/usr/bin/python3
"""Cree una nueva vista para objetos de places_r
que maneje todas las acciones predeterminadas
de la API RESTFul
"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, make_response, request, abort
from models.user import User
from models.place import Place
from models.review import Review


@app_views.route(
    '/places/<place_id>/reviews', methods=['GET'], strict_slashes=False
    )
def todosR(place_id):
    """ Todos los objetos de review """
    lugar = storage.get(Place, place_id)
    if not lugar:
        abort(404)
    reviews = [review.to_dict() for review in lugar.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def unitoR(review_id):
    """ retorna un objeto review """
    rev = storage.get(Review, review_id)
    if rev is None:
        abort(404)
    return jsonify(rev.to_dict())


@app_views.route(
    '/reviews/<review_id>', methods=["DELETE"], strict_slashes=False
    )
def eliminaR(review_id):
    """ Elimina un objeto """
    rev = storage.get(Review, review_id)
    if rev is None:
        abort(404)
    storage.delete(rev)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    "/places/<place_id>/reviews", methods=["POST"], strict_slashes=False
    )
def crearR(place_id):
    """ Crea un nuevo objeto ciudad """
    lugar = storage.get(Place, place_id)
    if lugar is None:
        abort(404)
    datos = request.get_json()
    if datos is None:
        abort(400, "Not a JSON")
    if "user_id" not in datos:
        abort(400, "Missing user_id")
    usu = storage.get(User, datos['user_id'])
    if usu is None:
        abort(404)
    if "text" not in datos:
        abort(400, "Missing text")
    datos["place_id"] = place_id
    nuevo = Review(**datos)
    nuevo.save()
    return make_response(jsonify(nuevo.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def putR(review_id):
    """ actualiza el objeto review """
    av = ["id", "user_id", "place_id", "created_at", "updated_at"]
    rev = storage.get(Review, review_id)
    if rev is None:
        abort(404)

    datos = request.get_json(silent=True)
    if datos is None:
        abort(400, "Not a JSON")
    for clave, valor in datos.items():
        if clave not in av:
            setattr(rev, clave, valor)
    storage.save()
    return make_response(jsonify(rev.to_dict()), 200)
