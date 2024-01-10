from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.internal import app
from src.internal.models.like import Like
from src.internal.models.rating import Rating
from src.internal.models.user import User
from src.internal.utils.access_controller import like_access_check
from src.internal.utils.status_messages import Status

@app.route('/api/v1/likes', methods=["POST"])
@jwt_required()
def create_like():
    try:
        current_user = get_jwt_identity()
        current_user = User.objects.get(username=current_user)
    except User.DoesNotExist:
        return Status.not_logged_in() #401 Unauthorized
    
    data = request.get_json()
    
    try:
        rating = Rating.objects.get(id=data["rating_id"])
    except User.DoesNotExist or Rating.DoesNotExist:
        return Status.not_found() #404 Not Found

    try:
        Like.objects.get(user_id=current_user.id, rating_id=rating.id)
    except Like.DoesNotExist:
        like = Like(user_id=current_user.id, rating_id=rating)
        like.save()
        return Status.created() #201 Created
    
    return Status.already_exists() #409 Conflict


@app.route('/api/v1/likes/<rating_id>:<user_id>', methods=["GET"])
def get_like_by_rating(rating_id, user_id):
    like = Like.objects.get(rating_id=rating_id, user_id= user_id)
    if like is None:
        return Status.not_found() #404 Not Found
    return jsonify(like) #200 OK


@app.route('/api/v1/likes/<id>', methods=["DELETE"])
@jwt_required()
def delete_like(id):
    try:
        current_user = get_jwt_identity()
        current_user = User.objects.get(username=current_user)
    except User.DoesNotExist:
        return Status.not_logged_in() #401 Unauthorized

    if like_access_check(current_user.id, id):
        return Status.does_not_have_access() #403 Forbidden

    like = Like.objects.get(id=id)
    like.delete()
    return Status.deleted() #200 OK
    
