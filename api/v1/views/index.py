#!/usr/bin/python3
""" index py """
from api.v1.views import app_views
from flask import jsonify, Blueprint, Flask
from models import storage


ObjectsObj = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}


@app_views.route('/status', strict_slashes=False)
def status():
    """ API's status """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def number_objects():
    """ retrieves number of objects by type """
    num_objs = {}
    for key, value in ObjectsObj.items():
        num_objs[key] = storage.count(value)
    return jsonify(num_objs)


if __name__ == "__main__":
    pass
