from flask import jsonify, request
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
    data = request.get_json()

    try:
        user = User.objects.get(username=data["username"])
        rating = Rating.objects.get(id=data["rating_id"])
    except User.DoesNotExist or Rating.DoesNotExist:
        return jsonify("User or rating does not exist")
    
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
    try:
        like = Like.objects.get(id=id)
        like.delete()
        return jsonify("Deleted like")
    
    except Like.DoesNotExist:
        return jsonify("Like does not exist")
    except Exception as e:
        return jsonify("Error deleting like")
