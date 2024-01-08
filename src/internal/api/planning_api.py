from bson import ObjectId
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus
from mongoengine import Q
from src.internal import app
from src.internal.models.beverage import Beverage
from src.internal.models.planning import Planning
from src.internal.models.user import User
from src.internal.utils.access_controller import admin_check
from src.internal.utils.status_messages import Status

@app.route('/api/v1/planning', methods=["POST"])
@jwt_required()
def create_planning():
    try:
        current_user = get_jwt_identity()
        current_user = User.objects.get(username=current_user)
    except User.DoesNotExist:
        # 401 Unauthorized
        return Status.not_logged_in()

    try:
        data = request.get_json()
        if check_beverage(str(data["beverage_id"])) is None:
            # 404 Not Found
            return Status.not_found()
        if check_beverage_in_planning(str(data["user_id"]), str(data["beverage_id"])) is None:
            new_planning = Planning(**data)
            new_planning.save()
            # 200 OK
            return Status.created()
        else:
            # 409 Already Exists
            return Status.already_exists()
    except Exception as e:
        # 500 Internal Server Error
        return Status.error()


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
        existing_beverage_in_planning = Planning.objects.get(user_id=user_id, beverage_id=beverage_id)
        return existing_beverage_in_planning
    except Planning.DoesNotExist:
        return None


@app.route('/api/v1/planning/<id>', methods=["GET"])
def get_planning(id):
    try:
        planning = Planning.objects.get(user_id=str(id))
        planning_data = [item.to_mongo().to_dict() for item in planning]
        return jsonify(planning_data), HTTPStatus.OK
    except Planning.DoesNotExist:
        return Status.not_found()
    except Exception as e:
        return Status.error()
    

@app.route('/api/v1/planning', methods=["GET"])
def get_all_plannings():
    try:
        query = request.args.get("q", type=str, default="")
        try:
            query = ObjectId(query)
            results = Planning.objects(Q(user_id__icontains=query)|Q(beverage_id__icontains=query)|Q(id__icontains=query))
            planningList = [planning.to_mongo().to_dict() for planning in results]
            # 200 OK
            return jsonify(planningList), HTTPStatus.OK
        except Exception:
            # 400 Bad Request
            return Status.bad_request()

    except Exception as e:
        return Status.error()


@app.route('/api/v1/planning/<id>', methods=["PUT"])
@jwt_required()
def update_planning(id):
    try:
        current_user = get_jwt_identity()
        current_user = User.objects.get(username=current_user)
    except User.DoesNotExist:
        # 401 Unauthorized
        return Status.not_logged_in()
    try:
        data = request.get_json()
        try:
            objectId = ObjectId(id)
            planning = Planning.objects.get(id=objectId)
            user_id_object = planning.user_id
            user_id = str(user_id_object.id)
        except Exception:
            # 404 Not Found
            return Status.error()
        if user_id == data["user_id"]:
            Planning.objects(id=objectId).update(set__beverage_id=ObjectId(data["beverage_id"]))
            # 200 OK
            return Status.updated()
        else:
            # 403
            return Status.Unauthorized
    except Exception:
        # 500 Internal server error
        return Status.error()


@app.route('/api/v1/planning/<id>', methods=["DELETE"])
@jwt_required()
def delete_planning(id):
    try:
        current_user = get_jwt_identity()
        current_user = User.objects.get(username=current_user)
    except User.DoesNotExist:
        # 401 Unauthorized
        return Status.not_logged_in()
    try:
        try:
            Planning.objects.get(id=str(id))
        except Exception:
            # 404 Not Found
            return Status.error()
        Planning.objects(id=str(id)).delete()
        # 200 OK
        return Status.deleted()
    except Exception:
        # 500 Internal server error
        return Status.error()
