from flask import jsonify, request
from datetime import datetime
from src.internal.models.like import Like
from src.internal.models.rating import Rating
from src.internal.models.user import User, UserProfile
from src.internal import app


@app.route("/api/v1/users/create", methods=["POST"])
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
    return jsonify("created")

def is_username_unique(username):
    existing_user = User.objects(username=username).first()
    return existing_user is None

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