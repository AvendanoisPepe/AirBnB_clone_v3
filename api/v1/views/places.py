#!/usr/bin/python3
"""Cree una nueva vista para objetos de places
que maneje todas las acciones predeterminadas
de la API RESTFul
"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, make_response, request, abort
from models.user import User
from models.city import City
from models.place import Place


@app_views.route(
    '/cities/<city_id>/places', methods=['GET'], strict_slashes=False
    )
def todosP(city_id):
    """ Todos los objetos de la ciudad """
    citi = storage.get(City, city_id)
    if not citi:
        abort(404)
    places = [place.to_dict() for place in citi.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def unitoP(place_id):
    """ retorna un objeto place """
    plac = storage.get(Place, place_id)
    if plac is None:
        abort(404)
    return jsonify(plac.to_dict())


@app_views.route(
    '/places/<place_id>', methods=["DELETE"], strict_slashes=False
    )
def eliminarP(place_id):
    """ Elimina un objeto """
    plac = storage.get(Place, place_id)
    if plac is None:
        abort(404)
    storage.delete(plac)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    "/cities/<city_id>/places", methods=["POST"], strict_slashes=False
    )
def crearP(city_id):
    """ Crea un nuevo objeto ciudad """
    citi = storage.get(City, city_id)
    if citi is None:
        abort(404)
    datos = request.get_json()
    if datos is None:
        abort(400, "Not a JSON")
    if "user_id" not in datos:
        abort(400, "Missing user_id")
    usu = storage.get(User, datos['user_id'])
    if usu is None:
        abort(404)
    if "name" not in datos:
        abort(400, "Missing name")
    datos["city_id"] = city_id
    nuevo = Place(**datos)
    nuevo.save()
    return make_response(jsonify(nuevo.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def putP(place_id):
    """ actualiza el objeto ciudad """
    av = ["id", "user_id", "city_id", "created_at", "updated_at"]
    lugar = storage.get(Place, place_id)
    if lugar is None:
        abort(404)

    datos = request.get_json(silent=True)
    if datos is None:
        abort(400, "Not a JSON")
    for clave, valor in datos.items():
        if clave not in av:
            setattr(lugar, clave, valor)
    storage.save()
    return make_response(jsonify(lugar.to_dict()), 200)
