# Python imports

# Framework imports
from flask import jsonify

from src.internal import app


@app.route('/api/v1/likes/create', methods=["POST"])
def create_like(data):
    """
    This API creates a new user
    :param data:
    :return:
    """
    return jsonify("Created like. NOT IMPLEMENTED")


@app.route('/api/v1/likes/get/<id>', methods=["GET"])
def get_like(id):
    """
    This API creates a new user
    :param id:
    :return:
    """
    return "Returned like. NOT IMPLEMENTED"


@app.route('/api/v1/likes/update', methods=["PUT"])
def update_like(data):
    """
    This API creates a new user
    :param data:
    :return:
    """
    return jsonify("Updated like. NOT IMPLEMENTED")


@app.route('/api/v1/likes/delete/<id>', methods=["DELETE"])
def delete_like(id):
    """
    This API creates a new user
    :param id:
    :return:
    """
    return jsonify("Deleted like. NOT IMPLEMENTED")
