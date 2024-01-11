from bson import ObjectId
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine import Q
from src.internal import app
from src.internal.models.beverage import Beverage
from src.internal.models.planning import Planning
from src.internal.models.user import User
from src.internal.utils.access_controller import admin_check
from src.internal.utils.status_messages import Status


@app.route("/api/v1/planning", methods=["POST"])
@jwt_required()
def create_planning():
    try:
        current_user = get_jwt_identity()
        current_user = User.objects.get(username=current_user)
    except User.DoesNotExist:
        return Status.not_logged_in()  # 401 Unauthorized

    try:
        data = request.get_json()

        try:
            Beverage.objects.get(id=str(data["beverage_id"]))
        except Beverage.DoesNotExist:
            return Status.not_found()  # 404 Not Found

        try:
            User.objects.get(id=str(data["user_id"]))
            if current_user.id != str(data["user_id"]) and not admin_check(current_user.id):
                return Status.does_not_have_access()  # 403 Forbidden
            try:
                Planning.objects.get(user_id=str(data["user_id"]), beverage_id=str(data["beverage_id"]))
                return Status.already_exists()  # 409 Conflict
            except Planning.DoesNotExist:
                newPlanning = Planning(**data)
                newPlanning.save()
                return Status.created()  # 201 Created
        except User.DoesNotExist:
            return Status.not_found()  # 404 Not Found
    except Exception:
        return Status.error()  # 500 Internal Server Error


@app.route("/api/v1/planning/<id>", methods=["GET"])
def get_planning(id):
    try:
        planning = Planning.objects.get(user_id=str(id))
        planning_data = [item.to_mongo().to_dict() for item in planning]
        return jsonify(planning_data)  # 200 OK

    except Planning.DoesNotExist:
        return Status.not_found()  # 404 Not Found
    except Exception:
        return Status.error()  # 500 Internal Server Error


@app.route("/api/v1/planning", methods=["GET"])
def get_all_plannings():
    try:
        query = ObjectId(request.args.get("q", type=str, default=""))
        results = Planning.objects(
            Q(user_id__icontains=query) | Q(beverage_id__icontains=query) | Q(id__icontains=query)
        )
        planningList = [planning.to_mongo().to_dict() for planning in results]
        return jsonify(planningList)  # 200 OK

    except Exception:
        return Status.bad_request()  # 400 Bad Request


@app.route("/api/v1/planning/<id>", methods=["PUT"])
@jwt_required()
def update_planning(id):
    try:
        current_user = get_jwt_identity()
        current_user = User.objects.get(username=current_user)
    except User.DoesNotExist:
        return Status.not_logged_in()  # 401 Unauthorized

    try:
        data = request.get_json()

        objectId = ObjectId(id)
        planning = Planning.objects.get(id=objectId)

        if planning.user_id.id == current_user.id or admin_check(current_user.id):
            planning.update(set__beverage_id=ObjectId(data["beverage_id"]))
            return Status.updated()  # 200 OK
        else:
            return Status.does_not_have_access()  # 403 Forbidden

    except Planning.DoesNotExist:
        return Status.not_found()  # 404 Not Found
    except Exception:
        return Status.error()  # 500 Internal Server Error


@app.route("/api/v1/planning/<id>", methods=["DELETE"])
@jwt_required()
def delete_planning(id):
    try:
        current_user = get_jwt_identity()
        current_user = User.objects.get(username=current_user)
    except User.DoesNotExist:
        return Status.not_logged_in()  # 401 Unauthorized

    try:
        plan = Planning.objects.get(id=str(id))

        if plan.user_id.id == current_user.id or admin_check(current_user.id):
            plan.delete()
            return Status.deleted()  # 200 OK
        else:
            return Status.does_not_have_access()  # 403 Forbidden

    except Planning.DoesNotExist:
        return Status.not_found()  # 404 Not Found
