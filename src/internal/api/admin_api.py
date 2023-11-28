# Python imports

# Framework imports
from flask import jsonify

from src.internal import app


@app.route('/api/v1/admin/create', methods=["POST"])
def create_admin(data):
    """
    This API creates a new user
    :param data:
    :return:
    """
    return jsonify("Created admin. NOT IMPLEMENTED")


@app.route('/api/v1/admin/get/<id>', methods=["GET"])
def get_admin(id):
    """
    This API creates a new user
    :param id:
    :return:
    """
    return "Returned admin. NOT IMPLEMENTED"

@app.route('/api/v1/admin/get', methods=["GET"])
def get_all_admin():
    return "Returned all admins. NOT IMPLEMENTED"


@app.route('/api/v1/admin/update', methods=["PUT"])
def update_admin(data):
    """
    This API creates a new user
    :param data:
    :return:
    """
    return jsonify("Updated admin. NOT IMPLEMENTED")


@app.route('/api/v1/admin/delete/<id>', methods=["DELETE"])
def delete_admin(id):
    """
    This API creates a new user
    :param id:
    :return:
    """
    return jsonify("Deleted admin. NOT IMPLEMENTED")
