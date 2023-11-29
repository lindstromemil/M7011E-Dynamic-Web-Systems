from flask import jsonify, request
from datetime import datetime, date, time, timezone
from src.internal import app
from src.internal.models.user import User, UserProfile


@app.route("/api/v1/users/create", methods=["POST"])
def create_user():
    """
    This API creates a new user
    :param jason data:
    :return:
    """
    data = request.get_json()
    if not is_username_unique(data["username"]):
        raise jsonify("name already exists")

    userProfile = UserProfile(image_path=data["image_path"], description=data["description"])
    user = User(username=data["username"], password=data["password"], created_at=datetime.now(), profile=userProfile)
    
    user.save()
    return jsonify("true")

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


@app.route("/api/v1/users/update", methods=["PUT"])
def update_user():
    """
    Update users data
    :param data:
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
        print (e)
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
