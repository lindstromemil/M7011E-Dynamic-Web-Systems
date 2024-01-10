from bson import ObjectId
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine import Q
from src.internal import app
from src.internal.models.beverage import Beverage
from src.internal.models.brand import Brand
from src.internal.models.user import User
from src.internal.models.rating import Rating
from src.internal.utils.access_controller import admin_check
from src.internal.utils.status_messages import Status


@app.route("/api/v1/beverages", methods=["POST"])
@jwt_required()
def create_beverage():
    try:
        current_user = get_jwt_identity()
        current_user = User.objects.get(username=current_user)
    except User.DoesNotExist:
        return Status.not_logged_in()  # 401 Unauthorized

    if admin_check(user_id=current_user.id):
        data = request.get_json()
        try:
            data["brand_id"] = Brand.objects.get(name=data["brand_id"])
        except Brand.DoesNotExist:
            return Status.brand_does_not_exist()  # 422 Unprocessable Entity
        try:
            beverage = Beverage.objects.get(name=data["name"])
            if beverage:
                return Status.name_already_in_use()  # 409 Conflict
        except Beverage.DoesNotExist:
            pass

        beverage = Beverage(**data)
        beverage.save()
        return Status.created()  # 201 Created
    else:
        return Status.does_not_have_access()  # 403 Forbidden


@app.route("/api/v1/beverages", methods=["GET"])
def get_beverage():
    query = request.args.get("q", type=str, default="")
    size = request.args.get("size", type=int, default=0)
    page = request.args.get("page", type=int, default=1)
    if page == 0:
        page = 1
    try:
        objectId = ObjectId(query)
        results = Beverage.objects(Q(id=objectId) | Q(brand_id=objectId))
    except Exception:
        results = Beverage.objects(
            Q(name__icontains=query) | Q(country__icontains=query) | Q(beverageType__icontains=query)
        )
    results = results.limit(size).skip((page - 1) * size)
    brandsList = [beverage.to_mongo().to_dict() for beverage in results]
    return jsonify(brandsList)  # 200 OK


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
        return jsonify(beverage)  # 200 OK
    except Beverage.DoesNotExist:
        return Status.not_found()  # 404 Not found
    except Exception:
        return Status.error()  # 500 Internal server error


@app.route("/api/v1/beverages/<name>", methods=["PATCH"])
@jwt_required()
def update_beverage(name):
    try:
        current_user = get_jwt_identity()
        current_user = User.objects.get(username=current_user)
    except User.DoesNotExist:
        return Status.not_logged_in()  # 401 Unauthorized

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
            return Status.updated()  # 200 OK

        except Beverage.DoesNotExist:
            return Status.not_found()  # 404 Not Found
        except Exception:
            return Status.error()  # 500 Internal Server Error
    else:
        return Status.does_not_have_access()  # 403 Forbidden


@app.route("/api/v1/beverages/<name>", methods=["DELETE"])
@jwt_required()
def delete_beverages(name):
    try:
        current_user = get_jwt_identity()
        current_user = User.objects.get(username=current_user)
    except User.DoesNotExist:
        return Status.not_logged_in()  # 401 Unauthorized

    if admin_check(current_user.id):
        try:
            try:
                objectId = ObjectId(name)
                beverage = Beverage.objects.get(id=objectId)
            except Exception:
                beverage = Beverage.objects.get(name=name)
            beverage.delete()
            return Status.deleted()  # 200 OK

        except Beverage.DoesNotExist:
            return Status.not_found()  # 404 Not Found
        except Exception:
            return Status.error()  # 500 Internal Server Error
    else:
        return Status.does_not_have_access()  # 403 Forbidden


@app.route("/api/v1/beverages/<id>/ratings", methods=["GET"])
def get_beverage_ratings(id):
    return jsonify(Rating.objects(beverage_id=id).all())  # 200 OK
