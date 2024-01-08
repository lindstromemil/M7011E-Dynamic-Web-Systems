from bson import ObjectId
from datetime import datetime
from flask import jsonify, request
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from http import HTTPStatus
from mongoengine import Q
from src.internal import app
from src.internal.models.follow import Followers, Follows
from src.internal.models.like import Like
from src.internal.models.rating import Rating
from src.internal.models.user import User, UserProfile
from src.internal.utils.access_controller import *
from src.internal.utils.status_messages import Status
import time

@app.route("/api/v1/users", methods=["POST"])
@cross_origin()
def create_user():
    data = request.get_json()
    if not is_username_unique(str(data["username"])):
        return Status.name_already_in_use()

    userProfile = UserProfile(image_path=data["image_path"], description=data["description"])
    user = User(username=data["username"], password=data["password"], created_at=datetime.now(), profile=userProfile)

    user.save()
    additional_claims = {"currentTime": user.created_at}
    access_token = create_access_token(identity=data["username"], additional_claims=additional_claims)
    return jsonify(access_token=access_token)


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
    if user is None:
        return Status.not_found()
    milli_sec = int(round(time.time() * 1000))
    additional_claims = {"currentTime": milli_sec}
    access_token = create_access_token(identity=user.username, additional_claims=additional_claims)
    return jsonify(access_token=access_token)


@app.route("/api/v1/users/me", methods=["GET"])
@jwt_required()
def get_me():
    """
    Get me
    :return user:
    """
    current_user = get_jwt_identity()

    user = User.objects(username=current_user).first()
    return jsonify(user)


@app.route("/api/v1/users/<name>", methods=["GET"])
def get_user(name):
    """
        Get user based on name
        :param name:
        :return User:
        """
    try:
        try:
            objectId = ObjectId(name)
            user = User.objects.get(id=objectId)
        except Exception:
            user = User.objects.get(name__icontains=name)
        # 200 OK
        return jsonify(user), HTTPStatus.OK
    except User.DoesNotExist:
        # 404 Not found
        return Status.not_found()
    except Exception:
        # 500 Internal server error
        return Status.error()


@app.route("/api/v1/users", methods=["GET"])
def get_all_user():
    """
        Gets all users matching a query if given
        :return User[]:
    """
    query = request.args.get("q", type=str, default="")
    size = request.args.get("size", type=int, default=0)
    page = request.args.get("page", type=int, default=1)
    if page == 0:
        page = 1

    try:
        objectId = ObjectId(query)
        results = User.objects(Q(id=objectId))
    except Exception:
        results = User.objects(Q(name__icontains=query))

    results = results.limit(size).skip((page - 1) * size)
    user_list = [brand.to_mongo().to_dict() for brand in results]
    # 200 OK
    return jsonify(user_list), HTTPStatus.OK


@app.route('/api/v1/users/<user_id>/likes', methods=["GET"])
def get_all_user_likes(user_id):
    all_likes = Like.objects(user_id=user_id)
    entries = []
    for item in all_likes:
        temp = [item.user_id, item.rating_id]
        entries.append(temp)

    return jsonify(entries)


@app.route("/api/v1/users/<user_id>", methods=["PATCH"])
@jwt_required()
def update_user(user_id):
    current_user = get_jwt_identity()
    data = request.get_json()

    if does_user_exist(current_user) is None:
        return Status.not_loged_in()

    if user_access_check(current_user, user_id):
        return Status.does_not_have_access()

    user = User.objects.get(id=user_id)
    for key, value in data.items():
        if key in user:
            setattr(user, key, value)
        elif key in user.profile:
            setattr(user.profile, key, value)

    user.save()
    return Status.updated()


@app.route("/api/v1/users/<name>", methods=["DELETE"])
@jwt_required()
def delete_user(name):
    current_user = get_jwt_identity()
    if does_user_exist(current_user) is None:
        return Status.not_loged_in()
    
    try:
        user = User.objects.get(username=name)
        if user_access_check(current_user, user.id):
            return Status.does_not_have_access()
    except User.DoesNotExist:
        return Status.not_found()

    user.delete()
    return Status.deleted()


@app.route('/api/v1/users/<name>/ratings', methods=["GET"])
def get_all_users_ratings(name):
    try:
        user_id = User.objects.get(username=name).id
    except User.DoesNotExist:
        return Status.not_found()
    
    return jsonify(Rating.objects(user_id=user_id))


@app.route('/api/v1/users/<name>/follows', methods=["GET"])
def get_user_follows_list(name):
    try:
        user = User.objects.get(username=name)
    except User.DoesNotExist:
        return Status.not_found()
    
    follows = Follows.objects.filter(user_id=user)
    entries = [follow.followed_id for follow in follows]

    return jsonify(entries)


@app.route('/api/v1/users/<name>/followers', methods=["GET"])
def get_user_followers_list(name):
    try:
        user = User.objects.get(username=name)
    except User.DoesNotExist:
        return Status.not_found()
    
    followed = Followers.objects.filter(user_id=user)
    entries = [follow.follower_id for follow in followed]

    return jsonify(entries)
