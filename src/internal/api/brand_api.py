from bson import ObjectId
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine import Q
from src.internal import app
from src.internal.models.brand import Brand
from src.internal.models.user import User
from src.internal.utils.access_controller import admin_check
from src.internal.utils.status_messages import Status


@app.route("/api/v1/brands", methods=["POST"])
@jwt_required()
def create_brand():
    try:
        current_user = get_jwt_identity()
        current_user = User.objects.get(username=current_user)
    except User.DoesNotExist:
        return Status.not_logged_in() #401 Unauthorized

    if admin_check(current_user.id):
        data = request.get_json()
        try:
            if Brand.objects.get(name=data["name"]):
                return Status.name_already_in_use() #409 Conflict
        except Brand.DoesNotExist:
            pass

        brand = Brand(**data)
        brand.save()
        return Status.created() #201 Created
    else:
        return Status.does_not_have_access() #403 Forbidden


@app.route("/api/v1/brands", methods=["GET"])
def get_all_brands():
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
    return jsonify(brandsList) #200 OK


@app.route("/api/v1/brands/<name>", methods=["GET"])
def get_brand(name):
    try:
        try:
            objectId = ObjectId(name)
            brand = Brand.objects.get(id=objectId)
        except Exception:
            brand = Brand.objects.get(name__icontains=name)
        return jsonify(brand) #200 OK
    except Brand.DoesNotExist:
        return Status.not_found() #404 Not found
    except Exception:
        return Status.error() #500 Internal server error


@app.route("/api/v1/brands/<name>", methods=["PATCH"])
@jwt_required()
def update_brand(name):
    try:
        current_user = get_jwt_identity()
        current_user = User.objects.get(username=current_user)
    except User.DoesNotExist:
        return Status.not_logged_in() #401 Unauthorized

    if admin_check(current_user.id):
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
            return Status.updated() #200 OK
        except Brand.DoesNotExist:
            return Status.not_found() #404 Not found
        except Exception:
            return Status.error() #500 Internal server error
    else:
        return Status.does_not_have_access() #403 Forbidden


@app.route("/api/v1/brands/<name>", methods=["DELETE"])
@jwt_required()
def delete_brand(name):
    try:
        current_user = get_jwt_identity()
        current_user = User.objects.get(username=current_user)
    except User.DoesNotExist:
        return Status.not_logged_in() #401 Unauthorized
    
    if admin_check(current_user.id):
        try:
            try:
                objectId = ObjectId(name)
                brand = Brand.objects.get(id=objectId)
            except Exception:
                brand = Brand.objects.get(name=name)
            brand.delete()
            return Status.deleted() #200 OK
        except Brand.DoesNotExist:
            return Status.not_found() #404 Not found
        except Exception:
            return Status.error() #500 Internal server error
    else:
        return Status.does_not_have_access() #403 Forbidden
