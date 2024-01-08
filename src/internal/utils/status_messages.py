from flask import jsonify, make_response
from http import HTTPStatus


class Status:
    # 200
    def ok():
        return make_response(jsonify({"message": "OK"}), HTTPStatus.OK)

    # 200
    def deleted():
        return make_response(jsonify({"message": "Deleted"}), HTTPStatus.OK)

    # 200
    def updated():
        return make_response(jsonify({"message": "Updated"}), HTTPStatus.OK)

    # 201
    def created():
        return make_response(jsonify({"message": "Created"}), HTTPStatus.CREATED)

    # 400
    def bad_request():
        return make_response(jsonify({"message": "The request is invalid"}), HTTPStatus.BAD_REQUEST)

    # 401
    def not_logged_in():
        return make_response(jsonify({"message": "No sender"}), HTTPStatus.UNAUTHORIZED)

    # 403
    def does_not_have_access():
        return make_response(jsonify({"message": "You do not have access"}), HTTPStatus.FORBIDDEN)

    # 404
    def not_found():
        return make_response(jsonify({"message": "Not found"}), HTTPStatus.NOT_FOUND)

    # 409
    def name_already_in_use():
        return make_response(jsonify({"message": "Name already exists"}), HTTPStatus.CONFLICT)

    # 409
    def already_a_admin():
        return make_response(jsonify({"message": "User is already a admin"}), HTTPStatus.CONFLICT)

    # 409
    def already_exists():
        return make_response(jsonify({"message": "Object / Connection already exists"}), HTTPStatus.CONFLICT)

    # 500
    def error():
        return make_response(
            jsonify({"message": "Something went wrong with the request"}), HTTPStatus.INTERNAL_SERVER_ERROR
        )
