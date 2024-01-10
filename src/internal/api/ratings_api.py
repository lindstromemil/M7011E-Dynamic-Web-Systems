from datetime import datetime
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus
from src.internal import app
from src.internal.models.beverage import Beverage
from src.internal.models.like import Like
from src.internal.models.rating import Rating
from src.internal.models.user import User
from src.internal.utils.access_controller import admin_check
from src.internal.utils.status_messages import Status


@app.route("/api/v1/ratings", methods=["POST"])
@jwt_required()
def create_rating():
    try:
        current_user = get_jwt_identity()
        current_user = User.objects.get(username=current_user)
    except User.DoesNotExist:
        # 401 Unauthorized
        return Status.not_logged_in()
    data = request.get_json()

    try:
        beverage = Beverage.objects.get(name=data["beverage"])
        rating = Rating(
            user_id=current_user,
            beverage_id=beverage,
            score=data["score"],
            comment=data["comment"],
            created_at=datetime.now(),
        )
        rating.save()
        return Status.created()
    except User.DoesNotExist or Beverage.DoesNotExist:
        return Status.not_found()
    except Exception as e:
        return Status.error()


# NOT NEEDED, only for testing
@app.route("/api/v1/ratings/<id>", methods=["GET"])
def get_rating(id):
    try:
        rating = Rating.objects(id=id).first()
        return jsonify(rating), HTTPStatus.OK
    except Rating.DoesNotExist:
        return Status.not_found()


# NOT NEEDED, only for testing
@app.route("/api/v1/ratings", methods=["GET"])
def get_all_ratings():
    return jsonify(Rating.objects().all()), HTTPStatus.OK


@app.route("/api/v1/ratings/<id>", methods=["PATCH"])
def update_rating(id):
    """
    Update ratings score or comment
    :param json data:
    :return:
    """
    try:
        current_user = get_jwt_identity()
        current_user = User.objects.get(username=current_user)
    except User.DoesNotExist:
        # 401 Unauthorized
        return Status.not_logged_in()

    try:
        rating = Rating.objects.get(id=id)
        if rating.user_id != current_user:
            if not admin_check(current_user.id):
                # 403 Forbidden
                return Status.does_not_have_access()
    except Rating.DoesNotExist:
        # 404 Not found
        return Status.not_found()

    data = request.get_json()
    for key, value in data.items():
        if key in rating and key != "id":
            setattr(rating, key, value)
    rating.save()
    # 200 OK
    return Status.updated()


@app.route("/api/v1/ratings/<id>", methods=["DELETE"])
@jwt_required()
def delete_rating(id):
    """
    Deletes rating based on id
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
        rating = Rating.objects.get(id=id)
    except Rating.DoesNotExist:
        # 404 Not found
        return Status.not_found()

    if admin_check(current_user.id) or current_user.id == rating.user_id:
        rating = Rating.objects.get(id=id)
        rating.delete()
        # 200 OK
        return Status.deleted()
    else:
        return Status.does_not_have_access()


@app.route("/api/v1/rating/<rating_id>/likes", methods=["GET"])
def get_all_rating_likes(rating_id):
    try:
        rating = Rating.objects.get(id=rating_id)
        all_likes = Like.objects(rating_id=rating_id)
        entries = []
        for item in all_likes:
            temp = [item.user_id, item.rating_id]
            entries.append(temp)
        return jsonify(entries), HTTPStatus.OK
    except Rating.DoesNotExist:
        return Status.not_found()
