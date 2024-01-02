# Python imports

# Framework imports
from http import HTTPStatus
from bson import ObjectId
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.internal.utils.access_controller import admin_check
from src.internal.utils.status_messages import Status
from mongoengine import Q
from src.internal.models.user import User

from src.internal import app

from src.internal.models.beverage import Beverage

from src.internal.models.brand import Brand


@app.route("/api/v1/beverages", methods=["POST"])
@jwt_required()
def create_beverage():
    """
    This API creates a new beverage

    Returns:
    """
    try:
        current_user = get_jwt_identity()
        current_user = User.objects.get(username=current_user)
    except User.DoesNotExist:
        # 401 Unauthorized
        return Status.not_logged_in()

    if admin_check(user_id=current_user.id):
        data = request.get_json()
        try:
            data["brand_id"] = Brand.objects.get(name=data["brand_id"])
        except Brand.DoesNotExist:
            return jsonify({"message": "Brand Does Not Exist, Please Enter Brand First"}), 422
        try:
            beverage = Beverage.objects.get(name=data["name"])
            if beverage:
                # 409 Conflict
                return Status.name_already_in_use()
        except Beverage.DoesNotExist:
            pass
        beverage = Beverage(**data)
        beverage.save()
        # 201 Created
        return Status.created()
    else:
        # 403 Forbidden
        return Status.does_not_have_access()


@app.route("/api/v1/beverages", methods=["GET"])
def get_beverage():
    query = request.args.get("q", type=str, default="")
    size = request.args.get("size", type=int, default=0)
    page = request.args.get("page", type=int, default=1)
    if page == 0:
        page = 1
    try:
        objectId = ObjectId(query)
        results = Beverage.objects(Q(id=objectId))
    except Exception:
        results = Beverage.objects(
            Q(name__icontains=query) | Q(country__icontains=query) | Q(beverageType__icontains=query)
        )
    results = results.limit(size).skip((page - 1) * size)
    brandsList = [beverage.to_mongo().to_dict() for beverage in results]
    # 200 OK
    return jsonify(brandsList), HTTPStatus.OK


@app.route("/api/v1/beverages/<name>", methods=["GET"])
def get_all_beverages(name):
    try:
        try:
            objectId = ObjectId(name)
            beverage = Beverage.objects.get(id=objectId)
        except Exception:
            beverage = Beverage.objects(
                Q(name__icontains=name) | Q(country__icontains=name) | Q(beverageType__icontains=name)
            ).first()
        # 200 OK
        return jsonify(beverage), HTTPStatus.OK
    except Beverage.DoesNotExist:
        # 404 Not found
        return Status.not_found()
    except Exception as e:
        print(e)
        # 500 Internal server error
        return Status.error()


@app.route("/api/v1/beverages/<name>", methods=["PATCH"])
@jwt_required()
def update_beverage(name):
    try:
        current_user = get_jwt_identity()
        current_user = User.objects.get(username=current_user)
    except User.DoesNotExist:
        # 401 Unauthorized
        return Status.not_logged_in()

    if admin_check(user_id=current_user.id):
        try:
            data = request.get_json()
            try:
                objectId = ObjectId(name)
                beverage = Beverage.objects.get(id=objectId)
            except Exception:
                beverage = Beverage.objects.get(name=name)
            for key, value in data.items():
                if key in beverage:
                    setattr(beverage, key, value)
            beverage.save()
            # 200 OK
            return Status.updated()
        except Beverage.DoesNotExist:
            # 404 Not found
            return Status.not_found()
        except Exception:
            # 500 Internal server error
            return Status.error()
    else:
        # 403 Forbidden
        return Status.does_not_have_access()


@app.route("/api/v1/beverages/<name>", methods=["DELETE"])
@jwt_required()
def delete_beverages(name):
    """
    Deletes brand based on name or id
    :param name:
    :return:
    """
    try:
        current_user = get_jwt_identity()
        current_user = User.objects.get(username=current_user)
    except User.DoesNotExist:
        # 401 Unauthorized
        return Status.not_logged_in()
    if admin_check(user_id=current_user.id):
        try:
            try:
                objectId = ObjectId(name)
                beverage = Beverage.objects.get(id=objectId)
            except Exception:
                beverage = Beverage.objects.get(name=name)
            beverage.delete()
            # 200 OK
            return Status.deleted()
        except Beverage.DoesNotExist:
            # 404 Not found
            return Status.not_found()
        except Exception:
            # 500 Internal server error
            return Status.error()
    else:
        # 403 Forbidden
        return Status.does_not_have_access()
