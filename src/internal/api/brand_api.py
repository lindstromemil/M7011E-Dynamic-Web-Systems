from flask import jsonify, request
from src.internal.models.brand import Brand
from src.internal import app


@app.route("/api/v1/brand/create", methods=["POST"])
def create_brand():
    """
    This API creates a new brand
    :param jason data:
    :return:
    """
    data = request.get_json()
    if not is_name_unique(data["name"]):
        raise jsonify("name already exists")
    
    brand = Brand(name=data["name"], description=data["description"])
    brand.save()
    return jsonify("true")

def is_name_unique(name):
    existing_name = Brand.objects(name=name).first()
    return existing_name is None

@app.route("/api/v1/brand/get/<name>", methods=["GET"])
def get_brand(name):
    """
    Get brand based on name
    :param name:
    :return:
    """
    brand = Brand.objects(name=name).first()
    return jsonify(brand)

@app.route("/api/v1/brand/get", methods=["GET"])
def get_all_brand():
    """
    Gets all brands
    :return All brands:
    """
    return jsonify(Brand.objects().all())


@app.route("/api/v1/brand/update", methods=["PUT"])
def update_brand():
    """
    This API creates a new user
    :param json data:
    :return:
    """
    data = request.get_json()
    try:
        brand = Brand.objects.get(id=data["id"])
        for key, value in data.items():
            if key in brand:
                setattr(brand, key, value)

        return jsonify("Updated brand")
    
    except Brand.DoesNotExist:
        return jsonify("Brand does not exist")
    except Exception as e:
        return jsonify("Error updating brand")


@app.route("/api/v1/brand/delete/<name>", methods=["DELETE"])
def delete_brand(name):
    """
    Deletes brand based on name
    :param name:
    :return:
    """
    try:
        brand = Brand.objects.get(name=name)
        brand.delete()
        return jsonify("Deleted brand")
    
    except Brand.DoesNotExist:
        return jsonify("User does not exist")
    except Exception as e:
        return jsonify("Error deleting user")
