#!/usr/bin/python3
""" Cities view module """
from models.amenity import Amenity
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask import make_response


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE'],
                 strict_slashes=False)
def cities_get_delete(state_id=None, city_id=None):
    """ Cities route """
    if state_id is not None:
        state = storage.get(State, state_id)
        # Return 404 if state_id not exists
        if state is None:
            abort(404)
        city_list = []
        for city in state.cities:
            city_list.append(city.to_dict())
        return jsonify(city_list)
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(city.to_dict())
    elif request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({})


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def city_post(state_id):
    """Cities POST Route"""
    obj = request.get_json()
    if obj is None:
        return make_response("Not a JSON", 400)
    if 'name' not in obj:
        return make_response("Missing name", 400)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    obj['state_id'] = state_id
    city = City(**obj)
    storage.new(city)
    storage.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def cities_put(city_id=None):
    """ Cities PUT route """
    ignore_keys = ['updated_at', 'created_at', 'id', 'state_id']
    obj = request.get_json()
    if obj is None:
        return make_response("Not a JSON", 400)
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for k, v in obj.items():
        if k not in ignore_keys:
            setattr(city, k, v)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
