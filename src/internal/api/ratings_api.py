from flask import jsonify, request
from datetime import datetime
from src.internal.models.like import Like
from src.internal.models.beverage import Beverage
from src.internal.models.rating import Rating
from src.internal.models.user import User

from src.internal import app


@app.route('/api/v1/ratings/create', methods=["POST"])
def create_rating():
    """
    This API creates a new rating
    :param json data:
    :return:
    """
    data = request.get_json()

    try:
        user_id = User.objects.get(username=data["username"]).id
        beverage_id = Beverage.objects.get(name=data["beverage"]).id
        rating = Rating(user_id=user_id, beverage_id=beverage_id, score=data["score"], comment=data["comment"], created_at=datetime.now())
        rating.save()
        return jsonify("created")
    
    except User.DoesNotExist or Beverage.DoesNotExist:
        return jsonify("User or Beverage does not exist")
    except Exception as e:
        return jsonify("Error creating rating")


@app.route('/api/v1/ratings/get/<id>', methods=["GET"])
def get_rating(id):
    """
    Get rating based on id
    :param id:
    :return rating:
    """
    rating = Rating.objects(id=id).first()
    return jsonify(rating)

@app.route('/api/v1/ratings/get', methods=["GET"])
def get_all_ratings():
    return jsonify(Rating.objects().all())

@app.route('/api/v1/ratings/likes/<rating_id>', methods=["GET"])
def get_all_rating_likes(rating_id):
    all_likes = Like.objects(rating_id=rating_id)
    entries = []
    for item in all_likes:
        temp = [item.user_id, item.rating_id]
        entries.append(temp)

    return jsonify(entries)

@app.route('/api/v1/ratings/update/<id>', methods=["PUT"])
def update_rating(id):
    """
    Update ratings score or comment
    :param json data:
    :return:
    """
    data = request.get_json()
    print(data)
    try:
        rating = Rating.objects.get(id=id)
        for key, value in data.items():
            if key is rating.score or rating.comment:
                setattr(rating, key, value)

        rating.save()
        return jsonify("Updated rating")
    
    except Rating.DoesNotExist:
        return jsonify("Rating does not exist")
    except Exception as e:
        return jsonify("Error updating rating")


@app.route('/api/v1/ratings/delete/<id>', methods=["DELETE"])
def delete_rating(id):
    """
    Deletes rating based on id
    :param id:
    :return:
    """
    try:
        rating = Rating.objects.get(id=id)
        rating.delete()
        return jsonify("Deleted rating")
    
    except Rating.DoesNotExist:
        return jsonify("Rating does not exist")
    except Exception as e:
        return jsonify("Error deleting rating")
