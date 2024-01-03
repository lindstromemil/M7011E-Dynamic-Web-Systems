# Python imports

# Framework imports
from flask import jsonify, request

from src.internal import app

from src.internal.models.planning import Planning

from src.internal.models.beverage import Beverage

from mongoengine import Q


@app.route('/api/v1/planning/create', methods=["POST"])
def create_planning():
    try:
        data = request.get_json()
        """if check_user(str(data["user_id"])) is not None:
            return jsonify({"message": "User already has a planning list"}"""
        if check_beverage(str(data["beverage_id"])) is None:
            return jsonify({"message": "Beverage does not exist"})
        if check_beverage_in_planning(str(data["user_id"]), str(data["beverage_id"])) is None:
            new_planning = Planning(**data)
            new_planning.save()
            return jsonify({"message": "Planning created successfully"}), 201
        else:
            return jsonify({"message": "Beverage already in planning for this user"}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def check_user(user_id):
    try:
        existing_user = Planning.objects.get(user_id=user_id)
        return existing_user
    except Exception as e:
        return None


def check_beverage(beverage_id):
    try:
        existing_beverage = Beverage.objects.get(id=beverage_id)
        return existing_beverage
    except Exception as e:
        return None


def check_beverage_in_planning(user_id, beverage_id):
    try:
        print("hejsan")
        existing_beverage_in_planning = Planning.objects.get(user_id=user_id, beverage_id=beverage_id)
        print(existing_beverage_in_planning.beverage_id, existing_beverage_in_planning.user_id)
        return existing_beverage_in_planning
    except Planning.DoesNotExist:
        return None


@app.route('/api/v1/planning/get/<id>', methods=["GET"])
def get_planning(id):
    try:
        planning = Planning.objects.filter(user_id=str(id))
        if planning:
            planning_data = [item.to_mongo().to_dict() for item in planning]
            return jsonify(planning_data)
        else:
            return jsonify({"No planning created for this user": str(e)}), 404
    except Exception as e:
        return jsonify({"Error": str(e)}), 500
    

@app.route('/api/v1/planning/get', methods=["GET"])
def get_all_plannings():
    return "Returned all plannings. NOT IMPLEMENTED"


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
