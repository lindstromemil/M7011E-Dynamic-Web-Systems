from flask import jsonify, request
from datetime import datetime
from src.internal.models.follow import FollowedBy, Follows
from src.internal.models.like import Like
from src.internal.models.rating import Rating
from src.internal.models.user import User, UserProfile
from src.internal import app
from flask_cors import cross_origin
from bson import ObjectId


@app.route("/api/v1/users/create", methods=["POST"])
@cross_origin()
def create_user():
    """
    This API creates a new user
    :param json data:
    :return:
    """
    data = request.get_json()
    if not is_username_unique(str(data["username"])):
        raise jsonify("name already exists")

    userProfile = UserProfile(image_path=data["image_path"], description=data["description"])
    user = User(username=data["username"], password=data["password"], created_at=datetime.now(), profile=userProfile)

    user.save()
    return jsonify(user)


def is_username_unique(username):
    existing_user = User.objects(username=username).first()
    return existing_user is None


@app.route("/api/v1/users/login/<username>:<password>", methods=["GET"])
def login_user(username, password):
    """
    Login user
    :param username:
    :param password:
    :return user:
    """
    user = User.objects(username=username, password=password).first()
    return jsonify(user)


@app.route("/api/v1/users/me", methods=["GET"])
def get_me():
    """
    Get me
    :return user:
    """
    data = request.headers
    id_string = data["Authorization"]
    _id = ObjectId(id_string)

    user = User.objects(id=_id).first()
    return jsonify(user)


@app.route("/api/v1/users/get/<name>", methods=["GET"])
def get_user(name):
    """
    Get user based on username
    :param username:
    :return user:
    """
    user = User.objects(username=name).first()
    return jsonify(user)


@app.route("/api/v1/users/get", methods=["GET"])
def get_all_user():
    """
    Gets all users
    :return All users:
    """
    return jsonify(User.objects().all())


@app.route('/api/v1/users/likes/<user_id>', methods=["GET"])
def get_all_user_likes(user_id):
    all_likes = Like.objects(user_id=user_id)
    entries = []
    for item in all_likes:
        temp = [item.user_id, item.rating_id]
        entries.append(temp)

    return jsonify(entries)


@app.route("/api/v1/users/update", methods=["PUT"])
def update_user():
    """
    Update users data
    :param json data:
    :return:
    """
    data = request.get_json()
    try:
        user = User.objects.get(id=data["id"])
        for key, value in data.items():
            if key in user:
                setattr(user, key, value)
            if key in user.profile:
                setattr(user.profile, key, value)

        user.save()
        return jsonify("Updated user")

    except User.DoesNotExist:
        return jsonify("User does not exist")
    except Exception as e:
        return jsonify("Error updating user")


@app.route("/api/v1/users/delete/<name>", methods=["DELETE"])
def delete_user(name):
    """
    Deletes user based on username
    :param username:
    :return:
    """
    try:
        user = User.objects.get(username=name)
        user.delete()
        return jsonify("Deleted user")

    except User.DoesNotExist:
        return jsonify("User does not exist")
    except Exception as e:
        return jsonify("Error deleting user")


@app.route('/api/v1/users/ratings/<name>', methods=["GET"])
def get_all_users_ratings(name):
    """
    Get all users ratings
    :param username:
    :return all ratings from user:
    """
    try:
        user_id = User.objects.get(username=name).id
    except User.DoesNotExist:
        return jsonify("user does not exist")

    return jsonify(Rating.objects(user_id=user_id))


@app.route('/api/v1/users/follows/<name>', methods=["GET"])
def get_user_follows_list(name):
    """
    Get all users followings
    :param username:
    :return list of all users the user is following:
    """
    try:
        user_id = User.objects.get(username=name)
    except User.DoesNotExist:
        return jsonify("user does not exist")

    follows = Follows.objects.filter(user_id=user_id)
    entries = [follow.followed_id for follow in follows]

    return jsonify(entries)


@app.route('/api/v1/users/followedby/<name>', methods=["GET"])
def get_user_followed_by_list(name):
    """
    Get all users followedby
    :param username:
    :return list of all users the user is followed by:
    """
    try:
        user_id = User.objects.get(username=name)
    except User.DoesNotExist:
        return jsonify("user does not exist")

    followed = FollowedBy.objects.filter(user_id=user_id)
    entries = [follow.follower_id for follow in followed]

    return jsonify(entries)
