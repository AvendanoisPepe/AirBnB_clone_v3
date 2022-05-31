#!/usr/bin/python3
"""Cree una nueva vista para objetos de usuarios
que maneje todas las acciones predeterminadas
de la API RESTFul
"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, make_response, request, abort
from models.user import User


@app_views.route(
    '/users', methods=['GET'], strict_slashes=False
    )
def todosU():
    """ Todos los objetos de usuarios """
    usuarios = []
    usu = storage.all(User).values()
    for user in usu:
        usuarios.append(user.to_dict())
    return jsonify(usuarios)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def unitoU(user_id):
    """ el objeto usuario solito """
    usu = storage.get(User, user_id)
    if usu is None:
        abort(404)
    return jsonify(usu.to_dict()), 200


@app_views.route(
    '/users/<user_id>', methods=["DELETE"], strict_slashes=False
    )
def eliminarU(user_id):
    """ Elimina un objeto """
    usu = storage.get(User, user_id)
    if usu is None:
        abort(404)
    storage.delete(usu)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def crearU():
    """ Crea un nuevo objeto usuario """
    datos = request.get_json(silent=True)
    if datos is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "email" not in datos:
        return ("Missing email", 400)
    elif "password" not in datos:
        return ("Missing password", 400)
    nuevo = User(**datos)
    nuevo.save()
    return make_response(jsonify(nuevo.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def putU(user_id):
    """ actualiza el objeto usuario """
    usu = storage.get(User, user_id)
    if usu is None:
        abort(404)
    datos = request.get_json(silent=True)
    if datos is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for clave, valor in datos.items():
        if clave not in ["id", "email", "created_at", "updated_at"]:
            setattr(usu, clave, valor)
    storage.save()
    return make_response(jsonify(usu.to_dict()), 200)
