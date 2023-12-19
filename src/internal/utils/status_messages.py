from http import HTTPStatus
from flask import jsonify, make_response


class Status():
    def created():
        return make_response(jsonify({"message" : "Created"}), HTTPStatus.CREATED)

    def deleted():
        return make_response(jsonify({"message" : "Deleted"}), HTTPStatus.OK)

    def updated():
        return make_response(jsonify({"message" : "Updated"}), HTTPStatus.OK)

    def error():
        return make_response(jsonify({"message" : "Something went wrong with the request"}), HTTPStatus.NOT_ACCEPTABLE)

    def not_found():
        return make_response(jsonify({"message" : "Not found"}), HTTPStatus.NOT_FOUND)

    def not_loged_in():
        return make_response(jsonify({"message" : "No sender"}), HTTPStatus.UNAUTHORIZED)

    def does_not_have_access():
        return make_response(jsonify({"message" : "You do not have access"}), HTTPStatus.FORBIDDEN)

    def name_already_in_use():
        return make_response(jsonify({"message": "Name already exists"}), HTTPStatus.BAD_REQUEST)
    
    def already_a_admin():
        return make_response(jsonify({"message": "User is already a admin"}), HTTPStatus.BAD_REQUEST)

