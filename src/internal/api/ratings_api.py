from datetime import datetime
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
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
        return Status.not_logged_in() #401 Unauthorized
    
    try:
        data = request.get_json()
        beverage = Beverage.objects.get(name=data["beverage"])
        rating = Rating(
            user_id=current_user,
            beverage_id=beverage,
            score=data["score"],
            comment=data["comment"],
            created_at=datetime.now(),
        )
        rating.save()
        return Status.created() #201 Created
    except User.DoesNotExist or Beverage.DoesNotExist:
        return Status.not_found() #404 Not Found
    except Exception:
        return Status.error() #500 Internal Server Error


@app.route("/api/v1/ratings/<id>", methods=["PATCH"])
def update_rating(id):
    try:
        current_user = get_jwt_identity()
        current_user = User.objects.get(username=current_user)
    except User.DoesNotExist:
        return Status.not_logged_in() #401 Unauthorized

    try:
        rating = Rating.objects.get(id=id)
        if rating.user_id != current_user:
            if not admin_check(current_user.id):
                return Status.does_not_have_access() #403 Forbidden
            
    except Rating.DoesNotExist:
        return Status.not_found() #404 Not Found

    data = request.get_json()
    for key, value in data.items():
        if key in rating and key != "id":
            setattr(rating, key, value)
    rating.save()
    return Status.updated() #200 OK


@app.route("/api/v1/ratings/<id>", methods=["DELETE"])
@jwt_required()
def delete_rating(id):
    try:
        current_user = get_jwt_identity()
        current_user = User.objects.get(username=current_user)
    except User.DoesNotExist:
        return Status.not_logged_in() #401 Unauthorized

    try:
        rating = Rating.objects.get(id=id)
    except Rating.DoesNotExist:
        return Status.not_found() #404 Not Found

    if admin_check(current_user.id) or current_user.id == rating.user_id:
        rating = Rating.objects.get(id=id)
        rating.delete()
        return Status.deleted() #200 OK
    else:
        return Status.does_not_have_access() #403 Forbidden


@app.route("/api/v1/rating/<rating_id>/likes", methods=["GET"])
def get_all_rating_likes(rating_id):
    try:
        rating = Rating.objects.get(id=rating_id)
        all_likes = Like.objects(rating_id=rating_id)
    except Rating.DoesNotExist or Like.DoesNotExist:
        return Status.not_found() #404 Not Found
    
    entries = []
    for item in all_likes:
        temp = [item.user_id, item.rating_id]
        entries.append(temp)
    return jsonify(entries) #200 OK
