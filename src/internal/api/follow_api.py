from flask import request
from src.internal.utils.status_messages import Status
from src.internal.utils.access_controller import admin_check, does_user_exist, follow_access_check, super_admin_check, user_access_check
from src.internal.models.follow import FollowedBy, Follows
from src.internal.models.user import User
from src.internal import app


@app.route('/api/v1/follow/create', methods=["POST"])
def create_follow():
    headers = request.headers
    data = request.get_json()

    if does_user_exist(headers["sender_id"]) is None:
        return Status.not_loged_in()

    try:
        first_user = User.objects.get(id=data["user_id"])
        second_user = User.objects.get(id=data["target_id"])
    except User.DoesNotExist:
        return Status.not_found()
    
    if user_access_check(headers["sender_id"], first_user.id):
        return Status.does_not_have_access()
    
    try:
        Follows.objects.get(user_id=first_user, followed_id=second_user)
        FollowedBy.objects.get(user_id=second_user, follower_id=first_user)
    except Follows.DoesNotExist or FollowedBy.DoesNotExist:
        follow = Follows(user_id=first_user, followed_id=second_user)
        followBy = FollowedBy(user_id=second_user, follower_id=first_user)
        follow.save()
        followBy.save()
        return Status.created()
    return Status.already_exists()


@app.route('/api/v1/follow/delete', methods=["DELETE"])
def delete_follow():
    headers = request.headers

    if does_user_exist(headers["sender_id"]) is None:
        return Status.not_loged_in()

    data = request.get_json()
    if follow_access_check(headers["sender_id"], data["user_id"], data["target_id"]):
        return Status.does_not_have_access()

    follow = Follows.objects.get(user_id=data["user_id"], followed_id=data["target_id"])
    followBy = FollowedBy.objects.get(user_id=data["target_id"], follower_id=data["user_id"])
    follow.delete()
    followBy.delete()
    return Status.deleted()

