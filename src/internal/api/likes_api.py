from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus
from src.internal import app
from src.internal.models.like import Like
from src.internal.models.rating import Rating
from src.internal.models.user import User
from src.internal.utils.access_controller import admin_check, like_access_check
from src.internal.utils.status_messages import Status

@app.route('/api/v1/likes', methods=["POST"])
@jwt_required()
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
    
    data = request.get_json()
    
    try:
        rating = Rating.objects.get(id=data["rating_id"])
    except User.DoesNotExist or Rating.DoesNotExist:
        # 404 Not Found
        return Status.not_found()

    try:
        Like.objects.get(user_id=current_user.id, rating_id=rating.id)
    except Like.DoesNotExist:
        like = Like(user_id=current_user.id, rating_id=rating)
        like.save()
        # 201 OK
        return Status.created()
    
    # 409 Conflict
    return Status.already_exists()


@app.route('/api/v1/likes/<id>', methods=["DELETE"])
@jwt_required()
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

    if like_access_check(current_user.id, id):
        return Status.does_not_have_access()

    try:
        like = Like.objects.get(id=id)
        like.delete()
        # 200 OK
        return Status.deleted()
    except Exception:
        # 500 Internal server error
        return Status.error()
