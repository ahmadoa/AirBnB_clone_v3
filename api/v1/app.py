#!/usr/bin/python3
""" flask framework app """
from models import storage
from api.v1.views import app_views
import os
from flask import Flask, render_template, make_response, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={"/*": {'origins': '0.0.0.0'}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(error):
    """ close storage method """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ 404 error """
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == "__main__":
    """ main method """
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(os.getenv('HBNB_API_PORT', 5000)), threaded=True)
