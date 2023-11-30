from flask import jsonify, request
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
    data = request.get_json()

    try:
        first_user = User.objects.get(username=data["yourUsername"])
        print(first_user)
        second_user = User.objects.get(username=data["targetUsername"])
        print(second_user)
    except User.DoesNotExist:
        return jsonify("A user does not exist")
    
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
    data = request.get_json()

    try:
        follow = Follows.objects.get(user_id=data["user_id"], followed_id=data["target_id"])
        followBy = FollowedBy.objects.get(user_id=data["target_id"], follower_id=data["user_id"])
        follow.delete()
        followBy.delete()
        return jsonify("Deleted follow")
    
    except Follows.DoesNotExist or FollowedBy.DoesNotExist:
        return jsonify("User is not following that target")
    except Exception as e:
        return jsonify("Error deleting follow")
