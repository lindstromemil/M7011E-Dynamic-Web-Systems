from bson import ObjectId
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine import Q
from src.internal import app
from src.internal.models.follow import Followers, Follows
from src.internal.models.user import User
from src.internal.utils.access_controller import admin_check
from src.internal.utils.status_messages import Status


@app.route("/api/v1/follows", methods=["POST"])
@jwt_required()
def create_follow():
    try:
        current_user = get_jwt_identity()
        current_user = User.objects.get(username=current_user)
    except User.DoesNotExist:
        return Status.not_logged_in() #401 Unauthorized

    data = request.get_json()
    try:
        target_user = User.objects.get(username=data["target_username"])
    except User.DoesNotExist:
        return Status.not_found() #404 Not Found

    if target_user.id == current_user.id:
        return Status.bad_request() #400 Bad Request

    try:
        Follows.objects.get(user_id=current_user.id, followed_id=target_user.id)
        Followers.objects.get(user_id=current_user.id, follower_id=target_user.id)
    except Follows.DoesNotExist or Followers.DoesNotExist:
        follow = Follows(user_id=current_user, followed_id=target_user)
        followBy = Followers(user_id=target_user, follower_id=current_user)
        follow.save()
        followBy.save()
        return Status.created() #201 Created
    return Status.already_exists() #409 Conflict


@app.route("/api/v1/follows", methods=["GET"])
def get_follows():
    query = request.args.get("q", type=str, default="")
    size = request.args.get("size", type=int, default=0)
    page = request.args.get("page", type=int, default=1)
    if page == 0:
        page = 1

    if query == "":
        return Status.bad_request() #400 Bad Request, Should not be empty

    try:
        objectId = ObjectId(query)
        results = Follows.objects(Q(user_id=objectId))
    except Exception:
        return Status.bad_request() #¤00 Bad Request

    results = results.limit(size).skip((page - 1) * size)
    usersList = [follow.followed_id.to_mongo().to_dict() for follow in results]
    return jsonify(usersList) #200 OK


@app.route("/api/v1/followers", methods=["GET"])
def get_followers():
    query = request.args.get("q", type=str, default="")
    size = request.args.get("size", type=int, default=0)
    page = request.args.get("page", type=int, default=1)
    if page == 0:
        page = 1

    if query == "":
        return Status.bad_request() #400 Bad Request, Should not be empty

    try:
        objectId = ObjectId(query)
        results = Followers.objects(Q(user_id=objectId))
    except Exception:
        return Status.bad_request() #400 Bad Request

    results = results.limit(size).skip((page - 1) * size)
    usersList = [follow.follower_id.to_mongo().to_dict() for follow in results]
    return jsonify(usersList) #200 OK


@app.route("/api/v1/follows/<name>", methods=["DELETE"])
@jwt_required()
def delete_follow(name):
    try:
        current_user = get_jwt_identity()
        current_user = User.objects.get(username=current_user)
    except User.DoesNotExist:
        return Status.not_logged_in() #401 Unauthorized

    try:
        try:
            objectId = ObjectId(name)
            follow = Follows.objects.get(user_id=current_user.id, followed_id=objectId)
            follower = Followers.objects.get(user_id=objectId, follower_id=current_user.id)
        except Exception:
            user = User.objects.get(username=name)
            follow = Follows.objects.get(user_id=current_user.id, followed_id=user.id)
            follower = Followers.objects.get(user_id=user.id, follower_id=current_user.id)

        follow.delete()
        follower.delete()
        return Status.deleted() #200 OK
    except Follows.DoesNotExist:
        return Status.not_found() #404 Not found
    except Exception:
        return Status.error() #500 Internal server error
