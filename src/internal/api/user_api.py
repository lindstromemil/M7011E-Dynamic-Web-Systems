from flask import jsonify, request
from datetime import datetime
from src.internal.utils.access_controller import *
from src.internal.utils.status_messages import Status
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
    data = request.get_json()
    if not is_username_unique(str(data["username"])):
        return Status.name_already_in_use()

    userProfile = UserProfile(image_path=data["image_path"], description=data["description"])
    user = User(username=data["username"], password=data["password"], created_at=datetime.now(), profile=userProfile)

    user.save()
    return Status.created()


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
    user = User.objects(username=name).first()
    return jsonify(user)


@app.route("/api/v1/users/get", methods=["GET"])
def get_all_user():
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
    headers = request.headers
    data = request.get_json()

    if does_user_exist(headers["sender_id"]) is None:
        return Status.not_loged_in()

    if user_access_check(headers["sender_id"], data["id"]):
        return Status.does_not_have_access()

    user = User.objects.get(id=data["id"])
    for key, value in data.items():
        if key in user:
            setattr(user, key, value)
        elif key in user.profile:
            setattr(user.profile, key, value)

    user.save()
    return Status.updated()


@app.route("/api/v1/users/delete/<name>", methods=["DELETE"])
def delete_user(name):
    headers = request.headers
    if does_user_exist(headers["sender_id"]) is None:
        return Status.not_loged_in()
    
    try:
        user = User.objects.get(username=name)
        if user_access_check(headers["sender_id"], user.id):
            return Status.does_not_have_access()
    except User.DoesNotExist:
        return Status.not_found()

    user.delete()
    return Status.deleted()


@app.route('/api/v1/users/ratings/<name>', methods=["GET"])
def get_all_users_ratings(name):
    try:
        user_id = User.objects.get(username=name).id
    except User.DoesNotExist:
        return Status.not_found()
    
    return jsonify(Rating.objects(user_id=user_id))


@app.route('/api/v1/users/follows/<name>', methods=["GET"])
def get_user_follows_list(name):
    try:
        user = User.objects.get(username=name)
    except User.DoesNotExist:
        return Status.not_found()
    
    follows = Follows.objects.filter(user_id=user)
    entries = [follow.followed_id for follow in follows]

    return jsonify(entries)


@app.route('/api/v1/users/followedby/<name>', methods=["GET"])
def get_user_followed_by_list(name):
    try:
        user = User.objects.get(username=name)
    except User.DoesNotExist:
        return Status.not_found()
    
    followed = FollowedBy.objects.filter(user_id=user)
    entries = [follow.follower_id for follow in followed]

    return jsonify(entries)
