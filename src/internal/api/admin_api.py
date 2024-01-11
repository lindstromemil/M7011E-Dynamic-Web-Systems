from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.internal import app
from src.internal.models.admin import Admin
from src.internal.models.user import User
from src.internal.utils.access_controller import admin_check, does_admin_exist, super_admin_check
from src.internal.utils.status_messages import Status


@app.route('/api/v1/admins', methods=["POST"])
@jwt_required()
def create_admin():
    try:
        current_user = get_jwt_identity()
        current_user = User.objects.get(username=current_user)
    except User.DoesNotExist:
        return Status.not_logged_in() #401 Unauthorized

    data = request.get_json()

    if admin_check(data["user_id"]):
        return Status.already_a_admin() #409 Conflict

    if (data["access"] == "admin") and admin_check(current_user.id):
        admin = Admin(user_id=data["user_id"], access=data["access"])
        admin.save()
        return Status.created() #201 Created

    if (data["access"] == "super_admin") and super_admin_check(current_user.id):
        admin = Admin(user_id=data["user_id"], access=data["access"])
        admin.save()
        return Status.created() #201 Created
    
    return Status.does_not_have_access() #403 Forbidden

@app.route("/api/v1/admins/me", methods=["GET"])
@jwt_required()
def admin_me():
    """
    Get me
    :return user:
    """
    try:
        current_user = get_jwt_identity()
        current_user = User.objects.get(username=current_user)
    except User.DoesNotExist:
        # 401 Unauthorized
        return Status.not_logged_in()
    try:
        admin = Admin.objects.get(user_id=current_user.id)
        return jsonify(True)
    except Exception:
        return jsonify(False)



@app.route('/api/v1/admins/me', methods=["POST"])
@jwt_required()
def super_admin_me():
    if (Admin.objects().count() == 0):
        try:
            current_user = get_jwt_identity()
            current_user = User.objects.get(username=current_user)
        except User.DoesNotExist:
            return Status.not_logged_in() #401 Unauthorized

        super = Admin(user_id=current_user.id, access="super_admin")
        super.save()
        return Status.created() #201 Created
    else:
        return Status.does_not_have_access() #403 Forbidden


@app.route('/api/v1/admins', methods=["GET"])
@jwt_required()
def get_all_admin():
    try:
        current_user = get_jwt_identity()
        current_user = User.objects.get(username=current_user)
    except User.DoesNotExist:
        return Status.not_logged_in() #401 Unauthorized

    if super_admin_check(current_user.id):
        return jsonify(Admin.objects().all()) #200 OK
    else:
        return Status.does_not_have_access() #403 Forbidden


@app.route('/api/v1/admins/<user_id>', methods=["PUT"])
@jwt_required()
def update_admin(user_id):
    try:
        current_user = get_jwt_identity()
        current_user = User.objects.get(username=current_user)
    except User.DoesNotExist:
        return Status.not_logged_in() #401 Unauthorized
    
    if does_admin_exist(user_id) is None:
        return Status.not_found() #404 Not Found
    
    data = request.get_json()
    
    if (super_admin_check(current_user.id)):
        admin = Admin.objects.get(user_id=user_id)
        if (data["access"] == "admin" or data["access"] == "super_admin"):
            setattr(admin, "access", data["access"])
            admin.save()
            return Status.updated() #200 OK
        else:
            return Status.bad_request() #400 Bad Request
    else:
        return Status.does_not_have_access() #403 Forbidden


@app.route('/api/v1/admins/<user_id>', methods=["DELETE"])
@jwt_required()
def delete_admin(user_id):
    try:
        current_user = get_jwt_identity()
        current_user = User.objects.get(username=current_user)
    except User.DoesNotExist:
        return Status.not_logged_in() #401 Unauthorized

    if does_admin_exist(user_id) is None:
        return Status.not_found() #404 Not Found

    if super_admin_check(current_user.id):
        admin = Admin.objects.get(user_id=user_id)
        admin.delete()
        return Status.deleted() #200 OK
    else:
        return Status.does_not_have_access() #403 Forbidden
