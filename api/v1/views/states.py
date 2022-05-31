#!/usr/bin/python3
"""Cree una nueva vista para objetos de estado que maneje
todas las acciones predeterminadas de la API RESTFul:
"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, make_response, request, abort
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def todos():
    """ Todos los objetos estado """
    return jsonify(
        [state.to_dict() for state in storage.all(State).values()]
        ), 200


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def unito(state_id):
    """ el objeto estado solito """
    estado = storage.get(State, state_id)
    if estado is None:
        return make_response(jsonify({"error": "Not found"}), 404)
    return jsonify(estado.to_dict()), 200


@app_views.route(
    '/states/<state_id>', methods=["DELETE"], strict_slashes=False
    )
def eliminar(state_id):
    """ Elimina un objeto """
    estado = storage.get(State, state_id)
    if estado is None:
        abort(404)
    storage.delete(estado)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def crear():
    """ Crea un nuevo objeto estado """
    datos = request.get_json(silent=True)
    if datos is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in datos:
        return ("Missing name", 400)
    nuevo = State(**datos)
    storage.new(nuevo)
    storage.save()
    return make_response(jsonify(nuevo.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def put(state_id):
    """ actualiza el objeto estado """
    estado = storage.get(State, state_id)
    if estado is None:
        abort(404)
    datos = request.get_json(silent=True)
    if datos is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for clave, valor in datos.items():
        if clave not in ["id", "created_at", "updated_at"]:
            setattr(estado, clave, valor)
    storage.save()
    return make_response(jsonify(estado.to_dict()), 200)
