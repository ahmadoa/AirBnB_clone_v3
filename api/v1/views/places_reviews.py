#!/usr/bin/python3
""" Module for storing indeces for the route to reviews. """
from flask import request, jsonify, abort, make_response
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from models.user import User
from models import storage


@app_views.route("/places/<place_id>/reviews", methods=["GET"])
def return_list_all_reviews_by_city(place_id):
    """ Returns reviews by place id. """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    list_reviews = place.reviews
    list_of_json_reviews = []
    for review in list_reviews:
        list_of_json_reviews.append(review.to_dict())
    return(jsonify(list_of_json_reviews), 200)


@app_views.route("/reviews/<review_id>", methods=["GET"])
def return_review_by_id(review_id):
    """ Returns review by id. """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return(jsonify(review.to_dict()), 200)


@app_views.route("/reviews/<review_id>", methods=["DELETE"])
def delete_review_obj(review_id):
    """ Deletes a review object by id. """
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return({}, 200)
    abort(404)


@app_views.route("/places/<place_id>/reviews", methods=["POST"])
def create_review_obj(place_id):
    """ Creates a new review linked to a place. """
    if storage.get(Place, place_id) is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return(make_response('Not a JSON', 400))
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if storage.get(User, data['user_id']) is None:
        abort(404)
    if 'text' not in data:
        abort(400, 'Missing text')
    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return(make_response(jsonify(review.to_dict()), 201))


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def update_review_obj(review_id):
    """ Updates a review by its id. """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return(make_response('Not a JSON', 400))
    ignored_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(review, key, value)
    storage.save()
    return(make_response(jsonify(review.to_dict()), 200))
