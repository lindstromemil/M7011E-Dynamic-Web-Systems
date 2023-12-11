# Python imports

# Framework imports
from flask import jsonify, request

from src.internal import app

from src.internal.models.beverage import Beverage

from src.internal.models.brand import Brand

import json


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
    existing_brand_name = Brand.objects.get(name=brand_name)
    return existing_brand_name

def does_beverage_exist(beverage_name):
    try:
        existing_beverage_name = Beverage.objects.get(name=beverage_name)
        return existing_beverage_name
    except Exception as e:
        return None


@app.route("/api/v1/beverage/get", methods=["GET"])
def get_beverage():
    try:
        data = request.get_json()
        queried_beverage = Beverage.objects.get(name=str(data["name"]))
        if queried_beverage is not None:
            return jsonify(queried_beverage,queried_beverage.brand_id)
        else:
            return jsonify({'message': 'Beverage not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/api/v1/beverage/get/all", methods=["GET"])
def get_all_beverages():
    try:
        beverages = Beverage.objects.all()
        return jsonify({'beverages': [beverage.to_json() for beverage in beverages]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/api/v1/beverage/update/<string:new_beverage_name>", methods=["PATCH"])
def update_beverage(new_beverage_name):
    try:
        data = request.get_json()
        update_data = {}
        if does_beverage_exist(str(data["name"])) is None:
            raise jsonify("Beverage Does Not Exist")

        Beverage.objects(name=str(data["name"])).update(**data)
        Beverage.objects(name=str(data["name"])).update(name=str(new_beverage_name))
        return jsonify({'message': 'Beverage updated successfully'}), 200
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
