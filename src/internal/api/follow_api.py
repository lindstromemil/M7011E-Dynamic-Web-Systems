# Python imports

# Framework imports
from flask import jsonify

from src.internal import app


@app.route('/api/v1/follow/create', methods=["POST"])
def create_follow(data):
    """
    This API creates a new user
    :param data:
    :return:
    """
    return jsonify("Created follow. NOT IMPLEMENTED")


@app.route('/api/v1/follow/get/<id>', methods=["GET"])
def get_follow(id):
    """
    This API creates a new user
    :param id:
    :return:
    """
    return "Returned follow. NOT IMPLEMENTED"


@app.route('/api/v1/follow/update', methods=["PUT"])
def update_follow(data):
    """
    This API creates a new user
    :param data:
    :return:
    """
    return jsonify("Updated follow. NOT IMPLEMENTED")


@app.route('/api/v1/follow/delete/<id>', methods=["DELETE"])
def delete_follow(id):
    """
    This API creates a new user
    :param id:
    :return:
    """
    return jsonify("Deleted follow. NOT IMPLEMENTED")
