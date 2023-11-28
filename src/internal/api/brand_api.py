# Python imports

# Framework imports
from flask import jsonify

from src.internal import app


@app.route("/api/v1/brand/create", methods=["POST"])
def create_brand(data):
    """
    This API creates a new user
    :param data:
    :return:
    """
    return jsonify("Created brand. NOT IMPLEMENTED")


@app.route("/api/v1/brand/get/<id>", methods=["GET"])
def get_brand(id):
    """
    This API creates a new user
    :param id:
    :return:
    """
    return "Returned brand. NOT IMPLEMENTED"


@app.route("/api/v1/brand/get", methods=["GET"])
def get_all_brand():
    return "Returned all brand. NOT IMPLEMENTED"


@app.route("/api/v1/brand/update", methods=["PUT"])
def update_brand(data):
    """
    This API creates a new user
    :param data:
    :return:
    """
    return jsonify("Updated brand. NOT IMPLEMENTED")


@app.route("/api/v1/brand/delete/<id>", methods=["DELETE"])
def delete_brand(id):
    """
    This API creates a new user
    :param id:
    :return:
    """
    return jsonify("Deleted brand. NOT IMPLEMENTED")
