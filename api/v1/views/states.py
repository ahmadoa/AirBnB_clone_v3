#!/usr/bin/python3
""" State view module """
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


@app_views.route('/states', strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET', 'DELETE'],
                 strict_slashes=False)
def route_states(state_id=None):
    """ States endpoint
    This is using docstrings for specifications.
    ---
    parameters:
      - name: state
        in: path
        type: string
        required: true
        default: all
    responses:
      200:
        description: A list of states
    """
    if state_id is None:
        all_states = storage.all(State)
        new_list = []
        for state in all_states.values():
            new_list.append(state.to_dict())
        return jsonify(new_list)
    state = storage.get(State, state_id)
    # Return 404 if state_id is not in storage
    if state is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(state.to_dict())
    elif request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return jsonify({})


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def state_post():
    """ States endpoint
    This is using docstrings for specifications.
    ---
    parameters:
      - name: state
        in: path
        type: string
        required: true
        default: all
    responses:
      200:
        description: A list of states
    """
    obj = request.get_json()
    if obj is None:
        return make_response("Not a JSON", 400)
    if 'name' not in obj:
        return make_response("Missing name", 400)
    state = State(**obj)
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def states_put(state_id=None):
    """ States endpoint
    This is using docstrings for specifications.
    ---
    parameters:
      - name: state
        in: path
        type: string
        required: true
        default: all
    responses:
      200:
        description: A list of states
    """
    obj = request.get_json()
    if obj is None:
        return make_response("Not a JSON", 400)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for k, v in obj.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(state, k, v)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
