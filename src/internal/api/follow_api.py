from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.internal.utils.status_messages import Status
from src.internal.utils.access_controller import (
    admin_check,
    does_user_exist,
    follow_access_check,
    super_admin_check,
    user_access_check,
)
from src.internal.models.follow import Followers, Follows
from src.internal.models.user import User
from src.internal import app


@app.route("/api/v1/follows", methods=["POST"])
@jwt_required()
def create_follow():
    try:
        current_user = get_jwt_identity()
        current_user = User.objects.get(username=current_user)
    except User.DoesNotExist:
        # 401 Unauthorized
        return Status.not_logged_in()

    data = request.get_json()
    try:
        target_user = User.objects.get(username=data["target_username"])
    except User.DoesNotExist:
        # 404 Not Found
        return Status.not_found()

    if target_user.id == current_user.id:
        return Status.bad_request()
    try:
        Follows.objects.get(user_id=first_user, followed_id=second_user)
        Followers.objects.get(user_id=second_user, follower_id=first_user)
    except Follows.DoesNotExist or Followers.DoesNotExist:
        follow = Follows(user_id=first_user, followed_id=second_user)
        followBy = Followers(user_id=second_user, follower_id=first_user)
        follow.save()
        followBy.save()
        return Status.created()
    return Status.already_exists()


@app.route("/api/v1/follow/delete", methods=["DELETE"])
def delete_follow():
    headers = request.headers

    if does_user_exist(headers["sender_id"]) is None:
        return Status.not_loged_in()

    data = request.get_json()
    if follow_access_check(headers["sender_id"], data["user_id"], data["target_id"]):
        return Status.does_not_have_access()

    follow = Follows.objects.get(user_id=data["user_id"], followed_id=data["target_id"])
    followBy = Followers.objects.get(user_id=data["target_id"], follower_id=data["user_id"])
    follow.delete()
    followBy.delete()
    return Status.deleted()
