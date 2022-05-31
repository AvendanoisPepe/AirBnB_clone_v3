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
    estado = storage.get(State, state_id)
    if estado is None:
        abort(404)
    return jsonify(
        [city.to_dict() for city in storage.all(City).values()]
        )


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
def post_city(state_id):
    """
    Creates a City
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = City(**data)
    instance.state_id = state.id
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


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
