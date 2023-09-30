#!/usr/bin/python3
""" user view module """
from api.v1.views import app_views
from models.user import User
from models import storage
from flask import Flask, jsonify, abort, request
from flask import make_response


@app_views.route('/users', strict_slashes=False)
@app_views.route('/users/<users_id>', methods=['GET', 'DELETE'])
def routu_users(users_id=None):
    """ user route """
    if users_id is None:
        all_users = storage.all(User)
        new_list = []
        for users in all_users.values():
            new_list.append(users.to_dict())
        return jsonify(new_list)
    users = storage.get(User, users_id)
#   Return 404 if user_id is not in storage
    if users is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(users.to_dict())
    elif request.method == 'DELETE':
        storage.delete(users)
        storage.save()
        return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def user_post():
    """user POST Route"""
    obj = request.get_json()
    if obj is None:
        return make_response("Not a JSON", 400)
    if 'email' not in obj:
        abort(400, 'Missing email')
    elif 'password' not in obj:
        abort(400, 'Missing password')
    user = User(**obj)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'])
def user_put(user_id=None):
    """Users PUT route """
    obj = request.get_json()
    if obj is None:
        return make_response("Not a JSON", 400)
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    for k, v in obj.items():
        if k not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, k, v)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
