# Python imports

# Framework imports
from flask import jsonify

from src.internal import app


@app.route("/api/v1/beverage/create", methods=["POST"])
def create_beverage(data):
    """
    This API creates a new user
    :param data:
    :return:
    """
    return jsonify("Created beverage. NOT IMPLEMENTED")


@app.route("/api/v1/beverage/get/<id>", methods=["GET"])
def get_beverage(id):
    """
    This API creates a new user
    :param id:
    :return:
    """
    return "Returned beverage. NOT IMPLEMENTED"


@app.route("/api/v1/beverage/get", methods=["GET"])
def get_all_beverages():
    return "Returned all beverages. NOT IMPLEMENTED"


@app.route("/api/v1/beverage/update", methods=["PUT"])
def update_beverage(data):
    """
    This API creates a new user
    :param data:
    :return:
    """
    return jsonify("Updated beverage. NOT IMPLEMENTED")


@app.route("/api/v1/beverage/delete/<id>", methods=["DELETE"])
def delete_beverages(id):
    """
    This API creates a new user
    :param id:
    :return:
    """
    return jsonify("Deleted beverage. NOT IMPLEMENTED")
