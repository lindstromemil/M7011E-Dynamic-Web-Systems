# Python imports

# Framework imports
from flask import jsonify, request

from src.internal import app

from src.internal.models.beverage import Beverage

from src.internal.models.brand import Brand


@app.route("/api/v1/beverage/create", methods=["POST"])
def create_beverage():
    try:
        data = request.get_json()

        if does_brand_exist(data["brand_id"]) is None:
            raise jsonify("Brand Does Not Exist, Please Enter Brand First")

        if does_beverage_exist(str(data["name"])):
            raise jsonify("Beverage Already Exists, Please Enter Unique Beverage")

        data["brand_id"] = Brand.objects.get(name=data["brand_id"])
        new_beverage = Beverage(**data)
        new_beverage.save()
        return jsonify({'message': 'Beverage created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def does_brand_exist(brand_name):
    existing_brand_name = Brand.objects.get(name__icontains=brand_name)
    return existing_brand_name


def does_beverage_exist(beverage_name):
    try:
        existing_beverage_name = Beverage.objects.get(name__icontains=beverage_name)
        return existing_beverage_name
    except Exception as e:
        return None


@app.route("/api/v1/beverage/get", methods=["GET"])
def get_beverage():
    try:
        data = request.get_json()
        queried_beverage = Beverage.objects.get(name=str(data["name"]))
        if queried_beverage is not None:
            return jsonify(queried_beverage, queried_beverage.brand_id)
        else:
            return jsonify({'message': 'Beverage not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def switch(body):
    query = {}
    if "name" in body:
        query["name__icontains"] = body["name"]
    if "beverageType" in body:
        query["beverageType__icontains"] = body["beverageType"]
    if "country" in body:
        query["country__icontains"] = body["country"]
    if "brand" in body:
        brand = does_brand_exist(body["brand"])
        query["brand_id__icontains"] = str(brand.id)
    return query


@app.route("/api/v1/beverage/get/all", methods=["GET"])
def get_all_beverages():
    try:
        data = request.get_json()
        query = switch(data)
        beverages = Beverage.objects(**query)
        all_beverages = [beverage.to_mongo().to_dict() for beverage in beverages]
        return jsonify(all_beverages)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/api/v1/beverage/update/", methods=["PATCH"])
def update_beverage():
    try:
        data = request.get_json()
        beverage_id = data["id"]
        del data["id"]
        Beverage.objects.get(id=beverage_id)
        Beverage.objects(id=beverage_id).update(**data)
        return jsonify({'message': 'Beverage updated successfully'}), 200
    except Beverage.DoesNotExist:
        return jsonify("Beverage Does Not Exist")
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/api/v1/beverage/delete/<id>", methods=["DELETE"])
def delete_beverages(id):
    try:
        beverage = Beverage.objects.get(id=id)
        beverage.delete()
        return jsonify({'message': 'Beverage deleted successfully'}), 200
    except Beverage.DoesNotExist:
        return jsonify({'error': 'Beverage not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
