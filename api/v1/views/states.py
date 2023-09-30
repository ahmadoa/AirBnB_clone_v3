#!/usr/bin/python3
""" objects that handle all default RestFul API actions for States """
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """ retrieves list of all states objects """
    all_states = storage.all(State).values()
    list_states = [state.to_dict() for state in all_states]
    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """ retrieves a specific state """
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ deletes a state object """
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ adding a new state """
    if not request.get_json():
        abort(400, 'Not a JSON')

    kwargs = request.get_json()
    if 'name' not in kwargs:
        abort(400, 'Missing name')

    state = State(**kwargs)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """ update a state object """
    state = storage.get(State, state_id)
    if state:
        if not request.get_json():
            abort(400, 'Not a JSON')

        data = request.get_json()
        ignore = ['id', 'create_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore:
                setattr(state, key, value)

        state.save()
        return jsonify(state.to_dict()), 200
    else:
        abort(404)
