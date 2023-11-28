# Python imports

# Framework imports
from flask import jsonify

from src.internal import app


@app.route('/api/v1/ratings/create', methods=["POST"])
def create_rating(data):
    """
    This API creates a new user
    :param data:
    :return:
    """
    return jsonify("Created rating. NOT IMPLEMENTED")


@app.route('/api/v1/ratings/get/<id>', methods=["GET"])
def get_rating(id):
    """
    This API creates a new user
    :param id:
    :return:
    """
    return "Returned rating. NOT IMPLEMENTED"

@app.route('/api/v1/ratings/get', methods=["GET"])
def get_all_ratings():
    return "Returned all ratings. NOT IMPLEMENTED"

@app.route('/api/v1/ratings/update', methods=["PUT"])
def update_rating(data):
    """
    This API creates a new user
    :param data:
    :return:
    """
    return jsonify("Updated rating. NOT IMPLEMENTED")


@app.route('/api/v1/ratings/delete/<id>', methods=["DELETE"])
def delete_rating(id):
    """
    This API creates a new user
    :param id:
    :return:
    """
    return jsonify("Deleted rating. NOT IMPLEMENTED")
