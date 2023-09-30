#!/usr/bin/python3
""" user view module """
from models import storage
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.user import User
from models.place import Place
from flask import Flask, jsonify, abort, request
from flask import make_response


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def route_users(place_id=None):
    """ place route """
    if place_id is not None:
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        new_list = []
        for review in place.reviews:
            new_list.append(review.to_dict())
        return jsonify(new_list)
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def route_review(review_id=None):
    """f694d9ce-2e60-44b1-95b0-2f4ebe2ed52d"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def route_delete(review_id=None):
    """f694d9ce-2e60-44b1-95b0-2f4ebe2ed52d"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def route_place_post(place_id):
    """State POST Route 32c11d3d-99a1-4406-ab41-7b6ccb7dd760 user
     place 3ebfaf23-cede-4cf0-964d-8afc17b11d02
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    obj = request.get_json()
    if obj is None:
        return make_response("Not a JSON", 400)
    if 'user_id' not in obj:
        abort(400, 'Missing user_id')
    user = storage.get(User, obj['user_id'])
    if user is None:
        abort(404)
    if 'text' not in obj:
        abort(400, 'Missing text')
    obj['place_id'] = place_id
    review = Review(**obj)
    storage.new(review)
    storage.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def reviews_put(review_id=None):
    """ States PUT route """
    ignore_keys = ['id', 'created_at', 'updated_at', 'place_id', 'user_id']
    obj = request.get_json()
    if obj is None:
        return make_response("Not a JSON", 400)
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    for k, v in obj.items():
        if k not in ignore_keys:
            setattr(review, k, v)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
