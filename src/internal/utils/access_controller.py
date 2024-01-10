from src.internal.models.admin import Admin
from src.internal.models.like import Like
from src.internal.models.user import User
from src.internal.utils.status_messages import Status


def does_admin_exist(admin_id):
    return Admin.objects.get(user_id=admin_id)


def admin_check(user_id):
    try:
        admin = Admin.objects.get(user_id=user_id)
        if admin.access == "admin" or admin.access == "super_admin":
            return True
        return False
    except Exception:
        return False


def super_admin_check(user_id):
    try:
        admin = Admin.objects.get(user_id=user_id)
        if admin.access == "super_admin":
            return True
        return False
    except Exception:
        return False


def user_access_check(username, user_id):
    try:
        current_user = User.objects.get(username=username)
        target_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Status.not_found()

    if current_user == target_user or admin_check(current_user.id) or super_admin_check(current_user.id):
        return False
    else:
        return True


def like_access_check(sender_id, like_id):
    try:
        user = User.objects.get(id=sender_id)
        like = Like.objects.get(id=like_id)
    except User.DoesNotExist:
        return Status.not_found()
    except Like.DoesNotExist:
        return Status.not_found()

    if user == like.user_id or admin_check(sender_id):
        return False
    else:
        return True
