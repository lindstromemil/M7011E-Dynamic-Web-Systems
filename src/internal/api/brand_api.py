from http import HTTPStatus
from bson import ObjectId
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine import Q
from src.internal.utils.access_controller import admin_check
from src.internal.models.brand import Brand
from src.internal.models.user import User
from src.internal import app
from src.internal.utils.status_messages import Status


@app.route("/api/v1/brands", methods=["POST"])
@jwt_required()
def create_brand():
    """
    This API creates a new brand
    :param json data:
    :return:
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
            if Brand.objects.get(name=data["name"]):
                # 409 Conflict
                return Status.name_already_in_use()
        except Brand.DoesNotExist:
            pass

        brand = Brand(**data)
        brand.save()
        # 201 Created
        return Status.created()
    else:
        # 403 Forbidden
        return Status.does_not_have_access()


@app.route("/api/v1/brands", methods=["GET"])
def get_all_brands():
    """
    Gets all brands matching a query if given
    :return brands[]:
    """
    query = request.args.get("q", type=str, default="")
    size = request.args.get("size", type=int, default=0)
    page = request.args.get("page", type=int, default=1)
    if page == 0:
        page = 1
    try:
        objectId = ObjectId(query)
        results = Brand.objects(Q(id=objectId))
    except Exception:
        results = Brand.objects(Q(name__icontains=query))

    results = results.limit(size).skip((page - 1) * size)
    brandsList = [brand.to_mongo().to_dict() for brand in results]
    # 200 OK
    return jsonify(brandsList), HTTPStatus.OK


@app.route("/api/v1/brands/<name>", methods=["GET"])
def get_brand(name):
    """
    Get brand based on name
    :param name:
    :return brand:
    """
    try:
        try:
            objectId = ObjectId(name)
            brand = Brand.objects.get(id=objectId)
        except Exception:
            brand = Brand.objects.get(name__icontains=name)
        # 200 OK
        return jsonify(brand), HTTPStatus.OK
    except Brand.DoesNotExist:
        # 404 Not found
        return Status.not_found()
    except Exception:
        # 500 Internal server error
        return Status.error()


@app.route("/api/v1/brands/<name>", methods=["PATCH"])
@jwt_required()
def update_brand(name):
    """
    Updates a brand
    :param json data:
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
            data = request.get_json()
            try:
                objectId = ObjectId(name)
                brand = Brand.objects.get(id=objectId)
            except Exception:
                brand = Brand.objects.get(name=name)
            for key, value in data.items():
                if key in brand and key != "id":
                    setattr(brand, key, value)
            brand.save()
            # 200 OK
            return Status.updated()
        except Brand.DoesNotExist:
            # 404 Not found
            return Status.not_found()
        except Exception:
            # 500 Internal server error
            return Status.error()
    else:
        # 403 Forbidden
        return Status.does_not_have_access()


@app.route("/api/v1/brands/<name>", methods=["DELETE"])
@jwt_required()
def delete_brand(name):
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
                brand = Brand.objects.get(id=objectId)
            except Exception:
                brand = Brand.objects.get(name=name)
            brand.delete()
            # 200 OK
            return Status.deleted()
        except Brand.DoesNotExist:
            # 404 Not found
            return Status.not_found()
        except Exception:
            # 500 Internal server error
            return Status.error()
    else:
        # 403 Forbidden
        return Status.does_not_have_access()
