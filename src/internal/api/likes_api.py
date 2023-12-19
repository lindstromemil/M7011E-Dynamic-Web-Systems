from flask import jsonify, request
from src.internal.utils.access_controller import does_user_exist, like_access_check, user_access_check
from src.internal.models.rating import Rating
from src.internal.models.like import Like
from src.internal.models.user import User
from src.internal import app


@app.route('/api/v1/likes/create', methods=["POST"])
def create_like():
    """
    This API creates a new like
    :param data:
    :return:
    """
    headers = request.headers
    data = request.get_json()

    if does_user_exist(headers["sender_id"]) is None:
        return jsonify("Sender does not exist")
    
    try:
        user = User.objects.get(username=data["username"])
        rating = Rating.objects.get(id=data["rating_id"])
    except User.DoesNotExist or Rating.DoesNotExist:
        return jsonify("User or rating does not exist")
    
    if user_access_check(headers["sender_id"], user.id):
        return jsonify("Does not have acces to create a follow for another user")

    try:
        Like.objects.get(user_id=user, rating_id=rating)
    except Like.DoesNotExist:
        like = Like(user_id=user, rating_id=rating)
        like.save()
        return jsonify("created")
    
    return jsonify("rating already liked by user")

#NOT NEEDED, only for testing
@app.route('/api/v1/likes/get/<id>', methods=["GET"])
def get_like(id):
    like = Like.objects(id=id).first()
    return jsonify(like)

#NOT NEEDED, not supposed to be allowed to update a like
@app.route('/api/v1/likes/update', methods=["PUT"])
def update_like(data):
    return jsonify("Updated like. NOT IMPLEMENTED")


@app.route('/api/v1/likes/delete/<id>', methods=["DELETE"])
def delete_like(id):
    """
    Delete / remove a like
    :param id:
    :return:
    """
    headers = request.headers
    if does_user_exist(headers["sender_id"]) is None:
        return jsonify("Sender does not exist")

    if like_access_check(headers["sender_id"], id):
        return jsonify("Does not have access")
    
    like = Like.objects.get(id=id)
    like.delete()
    return jsonify("Deleted like")
