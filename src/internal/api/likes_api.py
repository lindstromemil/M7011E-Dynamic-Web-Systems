from flask import jsonify, request
from src.internal.utils.access_controller import does_user_exist, like_access_check, user_access_check
from src.internal.models.rating import Rating
from src.internal.models.like import Like
from src.internal.models.user import User
from src.internal import app
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.internal.utils.status_messages import Status
from http import HTTPStatus


@app.route('/api/v1/likes/create', methods=["POST"])
def create_like():
    """
    This API creates a new like
    :param data:
    :return:
    """
    try:
        current_user = get_jwt_identity()
        current_user = User.objects.get(username=current_user)
    except User.DoesNotExist:
        # 401 Unauthorized
        return Status.not_logged_in()

    headers = request.headers
    data = request.get_json()

    if does_user_exist(headers["sender_id"]) is None:
        # 404 Not Found
        return Status.not_found()
    
    try:
        user = User.objects.get(username=data["username"])
        rating = Rating.objects.get(id=data["rating_id"])
    except User.DoesNotExist or Rating.DoesNotExist:
        # 404 Not Found
        return Status.not_found()

    try:
        Like.objects.get(user_id=user, rating_id=rating)
    except Like.DoesNotExist:
        like = Like(user_id=user, rating_id=rating)
        like.save()
        # 201 OK
        return Status.created()
    
    # 409 Conflict
    return Status.already_exists()

#NOT NEEDED, only for testing
@app.route('/api/v1/likes/get/<id>', methods=["GET"])
def get_like(id):
    try:
        like = Like.objects(id=id).first()
        return jsonify(like), HTTPStatus.OK
    except Exception:
        # 400 Bad Request
        return Status.bad_request()

#NOT NEEDED, not supposed to be allowed to update a like
@app.route('/api/v1/likes/update', methods=["PUT"])
def update_like(data):
    return jsonify("Updated like. NOT IMPLEMENTED")


@app.route('/api/v1/likes/delete/<id>', methods=["DELETE"])
def delete_like(id):
    """
    Delete / remove a like
    :param id:
    :return:
    """
    try:
        current_user = get_jwt_identity()
        current_user = User.objects.get(username=current_user)
    except User.DoesNotExist:
        # 401 Unauthorized
        return Status.not_logged_in()
    try:
        headers = request.headers
        if does_user_exist(headers["sender_id"]) is None:
            # 404 Not found
            return Status.not_found()
        
        like = Like.objects.get(id=id)
        like.delete()
        # 200 OK
        return Status.deleted()
    except Exception:
        # 500 Internal server error
        return Status.error()
