# Python imports

# Framework imports
from flask import jsonify

from src.internal import app


@app.route('/api/v1/users/create', methods=["POST"])
def create_user(data):
    """
    This API creates a new user
    :param data:
    :return:
    """
    return jsonify("Created user. NOT IMPLEMENTED")


@app.route('/api/v1/users/get/<id>', methods=["GET"])
def get_user(id):
    """
    This API creates a new user
    :param id:
    :return:
    """
    return "Returned user. NOT IMPLEMENTED"


@app.route('/api/v1/users/update', methods=["PUT"])
def update_user(data):
    """
    This API creates a new user
    :param data:
    :return:
    """
    return jsonify("Updated user. NOT IMPLEMENTED")


@app.route('/api/v1/users/delete/<id>', methods=["DELETE"])
def delete_user(id):
    """
    This API creates a new user
    :param id:
    :return:
    """
    return jsonify("Deleted user. NOT IMPLEMENTED")
