# Python imports

# Framework imports
from flask import jsonify

from src.internal import app


@app.route('/api/v1/spirits/create', methods=["POST"])
def create_spirit(data):
    """
    This API creates a new user
    :param data:
    :return:
    """
    return jsonify("Created spirit. NOT IMPLEMENTED")


@app.route('/api/v1/spirits/get/<id>', methods=["GET"])
def get_spirit(id):
    """
    This API creates a new user
    :param id:
    :return:
    """
    return "Returned spirit. NOT IMPLEMENTED"


@app.route('/api/v1/spirits/update', methods=["PUT"])
def update_spirits(data):
    """
    This API creates a new user
    :param data:
    :return:
    """
    return jsonify("Updated spirit. NOT IMPLEMENTED")


@app.route('/api/v1/spirits/delete/<id>', methods=["DELETE"])
def delete_spirits(id):
    """
    This API creates a new user
    :param id:
    :return:
    """
    return jsonify("Deleted spirit. NOT IMPLEMENTED")
