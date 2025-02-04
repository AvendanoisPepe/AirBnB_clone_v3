#!/usr/bin/python3
"""Cree una nueva vista para objetos de ciudad
que maneje todas las acciones predeterminadas
de la API RESTFul
"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, make_response, request, abort
from models.state import State
from models.city import City


@app_views.route(
    '/states/<state_id>/cities', methods=['GET'], strict_slashes=False
    )
def todosC(state_id):
    """ Todos los objetos de la ciudad """
    list_cities = []
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    for city in state.cities:
        list_cities.append(city.to_dict())

    return jsonify(list_cities)


@app_views.route('cities/<city_id>', methods=['GET'], strict_slashes=False)
def unitoC(city_id):
    """ un objeto ciudad """
    ciudad = storage.get(City, city_id)
    if ciudad is None:
        abort(404)
    return jsonify(ciudad.to_dict())


@app_views.route(
    '/cities/<city_id>', methods=["DELETE"], strict_slashes=False
    )
def eliminarC(city_id):
    """ Elimina un objeto """
    ciudad = storage.get(City, city_id)
    if ciudad is None:
        abort(404)
    storage.delete(ciudad)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    "/states/<state_id>/cities", methods=["POST"], strict_slashes=False
    )
def crearC(state_id):
    """ Crea un nuevo objeto ciudad """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    datos = request.get_json()
    if datos is None:
        abort(400, "Not a JSON")
    if "name" not in datos:
        abort(400, "Missing name")
    nuevo = City(**datos)
    nuevo.state_id = state_id
    nuevo.save()
    return make_response(jsonify(nuevo.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def putC(city_id):
    """ actualiza el objeto ciudad """
    ciudad = storage.get(City, city_id)
    if ciudad is None:
        abort(404)

    datos = request.get_json(silent=True)
    if datos is None:
        abort(400, "Not a JSON")
    for clave, valor in datos.items():
        if clave not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(ciudad, clave, valor)
    storage.save()
    return make_response(jsonify(ciudad.to_dict()), 200)
