from flask import jsonify, request
from src.internal.utils.access_controller import admin_check, does_user_exist, follow_access_check, super_admin_check, user_access_check
from src.internal.models.follow import FollowedBy, Follows
from src.internal.models.user import User
from src.internal import app


@app.route('/api/v1/follow/create', methods=["POST"])
def create_follow():
    """
    This API creates a new following
    :param json data:
    :return:
    """
    headers = request.headers
    data = request.get_json()

    if does_user_exist(headers["sender_id"]) is None:
        return jsonify("Sender does not exist")

    try:
        first_user = User.objects.get(username=data["yourUsername"])
        second_user = User.objects.get(username=data["targetUsername"])
    except User.DoesNotExist:
        return jsonify("A user does not exist")
    
    if user_access_check(headers["sender_id"], first_user.id):
        return jsonify("Does not have acces to create a follow for another user")
    
    try:
        Follows.objects.get(user_id=first_user, followed_id=second_user)
        FollowedBy.objects.get(user_id=second_user, follower_id=first_user)
    except Follows.DoesNotExist or FollowedBy.DoesNotExist:
        follow = Follows(user_id=first_user, followed_id=second_user)
        followBy = FollowedBy(user_id=second_user, follower_id=first_user)
        follow.save()
        followBy.save()
        return jsonify("created")
    
    return jsonify("User is already following that person")


#NOT NEEDED, only for testing
@app.route('/api/v1/follow/get/<id>', methods=["GET"])
def get_follow(id):
    follow = Follows.objects(id=id).first()
    return jsonify(follow)


#NOT NEEDED, not supposed to be allowed to update a follow
@app.route('/api/v1/follow/update', methods=["PUT"])
def update_follow():
    return jsonify("Updated follow. NOT IMPLEMENTED")


@app.route('/api/v1/follow/delete', methods=["DELETE"])
def delete_follow():
    """
    Deletes a following connection betew two users
    :param json data:
    :return:
    """
    headers = request.headers
    if does_user_exist(headers["sender_id"]) is None:
        return jsonify("Sender does not exist")
    
    data = request.get_json()
    if follow_access_check(headers["sender_id"], data["user_id"], data["target_id"]):
        return jsonify("Does not have access")
    
    follow = Follows.objects.get(user_id=data["user_id"], followed_id=data["target_id"])
    followBy = FollowedBy.objects.get(user_id=data["target_id"], follower_id=data["user_id"])
    follow.delete()
    followBy.delete()
    return jsonify("Deleted follow")
