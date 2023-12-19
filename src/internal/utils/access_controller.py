from flask import jsonify
from src.internal.models.admin import Admin
from src.internal.models.follow import FollowedBy, Follows
from src.internal.models.like import Like
from src.internal.models.rating import Rating
from src.internal.models.user import User


def does_user_exist(user_id):
    return User.objects.get(id=user_id)

def does_admin_exist(admin_id):
    return Admin.objects.get(id=admin_id)

def admin_check(user_id):
    try:
        admin = Admin.objects.get(id=user_id)
        if (admin.access == "admin"):
            return True
        return False
    except Exception as e:
        return False

def super_admin_check(user_id):
    try:
        admin = Admin.objects.get(id=user_id)
        if (admin.access == "super_admin"):
            return True
        return False
    except Exception as e:
        return False


def user_access_check(sender_id, user_id):
    try:
        current_user = User.objects.get(id=sender_id)
        target_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return jsonify("User does not exist")
    
    if (current_user == target_user or admin_check(current_user.id) or super_admin_check(current_user.id)):
        return False
    else:
        return True


def ratings_access_check(sender_id, rating_id):
    try:
        current_user = User.objects.get(id=sender_id)
        target_rating = Rating.objects.get(id=rating_id)
    except User.DoesNotExist:
        return jsonify("User does not exist")
    except Rating.DoesNotExist:
        return jsonify("Rating does not exist")
    
    if (current_user == target_rating.user_id or admin_check(current_user.id) or super_admin_check(current_user.id)):
        return False
    else:
        return True
    
def follow_access_check(sender_id, user_id, targeted_id):
    try:
        follow = Follows.objects.get(user_id=user_id, followed_id=targeted_id)
        followBy = FollowedBy.objects.get(user_id=targeted_id, follower_id=user_id)
    except Follows.DoesNotExist:
        return jsonify("Follow does not exist")
    except FollowedBy.DoesNotExist:
        return jsonify("FolloedBy does not exist")
    
    if (sender_id == follow.id or admin_check(sender_id) or super_admin_check(sender_id)):
        return False
    else:
        return True
    
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