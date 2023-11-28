# Python imports

# Framework imports
from flask import jsonify

from src.internal import app


@app.route('/api/v1/planning/create', methods=["POST"])
def create_planning(data):
    """
    This API creates a new user
    :param data:
    :return:
    """
    return jsonify("Created planning. NOT IMPLEMENTED")


@app.route('/api/v1/planning/get/<id>', methods=["GET"])
def get_planning(id):
    """
    This API creates a new user
    :param id:
    :return:
    """
    return "Returned planning. NOT IMPLEMENTED"


@app.route('/api/v1/planning/update', methods=["PUT"])
def update_planning(data):
    """
    This API creates a new user
    :param data:
    :return:
    """
    return jsonify("Updated planning. NOT IMPLEMENTED")


@app.route('/api/v1/planning/delete/<id>', methods=["DELETE"])
def delete_planning(id):
    """
    This API creates a new user
    :param id:
    :return:
    """
    return jsonify("Deleted planning. NOT IMPLEMENTED")
