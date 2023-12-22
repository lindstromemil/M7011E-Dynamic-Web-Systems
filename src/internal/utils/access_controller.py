from flask import jsonify
from src.internal.utils.status_messages import Status
from src.internal.models.admin import Admin
from src.internal.models.follow import Followers, Follows
from src.internal.models.like import Like
from src.internal.models.rating import Rating
from src.internal.models.user import User


def does_user_exist(username):
    return User.objects.get(username=username)

def does_admin_exist(admin_id):
    return Admin.objects.get(user_id=admin_id)

def admin_check(user_id):
    try:
        admin = Admin.objects.get(user_id=user_id)
        if (admin.access == "admin"):
            return True
        return False
    except Exception as e:
        return False

def super_admin_check(user_id):
    try:
        admin = Admin.objects.get(user_id=user_id)
        if (admin.access == "super_admin"):
            return True
        return False
    except Exception as e:
        return False


def user_access_check(username, user_id):
    try:
        current_user = User.objects.get(username=username)
        target_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Status.not_found()
    
    if (current_user == target_user or admin_check(current_user.id) or super_admin_check(current_user.id)):
        return False
    else:
        return True


def ratings_access_check(sender_id, rating_id):
    try:
        current_user = User.objects.get(id=sender_id)
        target_rating = Rating.objects.get(id=rating_id)
    except User.DoesNotExist:
        return Status.not_found()
    except Rating.DoesNotExist:
        return Status.not_found()
    
    if (current_user == target_rating.user_id or admin_check(current_user.id) or super_admin_check(current_user.id)):
        return False
    else:
        return True
    
def follow_access_check(sender_id, user_id, target_id):
    try:
        follow = Follows.objects.get(user_id=user_id, followed_id=target_id)
        followBy = Followers.objects.get(user_id=target_id, follower_id=user_id)
        if ((sender_id == user_id) or admin_check(sender_id) or super_admin_check(sender_id)):
            return False
        else:
            return True
    except Follows.DoesNotExist:
        return Status.not_found()
    except Followers.DoesNotExist:
        return Status.not_found()
    
def like_access_check(sender_id, like_id):
    try:
        user = User.objects.get(id=sender_id)
        like = Like.objects.get(id=like_id)
    except User.DoesNotExist:
        return jsonify("User does not exist")
    except Like.DoesNotExist:
        return jsonify("Like does not exist")
    
    if (user == like.user_id or admin_check(sender_id) or super_admin_check(sender_id)):
        return False
    else:
        return True