from flask import jsonify, request
from src.internal.utils.access_controller import admin_check, does_admin_exist, does_user_exist, super_admin_check
from src.internal.utils.status_messages import Status
from src.internal.models.admin import Admin
from src.internal import app


@app.route('/api/v1/admin/create', methods=["POST"])
def create_admin():
    headers = request.headers
    data = request.get_json()
    
    existing_user = does_user_exist(data["user_id"])
    if existing_user is None:
        return Status.not_found()

    if admin_check(existing_user.id) or super_admin_check(existing_user.id):
        return Status.already_a_admin()

    if (data["access"] == "admin") and (admin_check(headers["sender_id"]) or super_admin_check(headers["sender_id"])):
        admin = Admin(user_id=existing_user, access=data["access"])
        admin.save()
        return Status.created()

    if (data["access"] == "super_admin") and super_admin_check(headers["sender_id"]):
        admin = Admin(user_id=existing_user, access=data["access"])
        admin.save()
        return Status.created()
    
    return Status.does_not_have_access()


@app.route('/api/v1/admin/me', methods=["POST"])
def super_admin_me():
    if (Admin.objects().count() == 0):
        headers = request.headers
        super = Admin(user_id=headers["sender_id"], access="super_admin")
        super.save()
        return Status.created()
    else:
        return Status.does_not_have_access()


@app.route('/api/v1/admin/get/<admin_id>', methods=["GET"])
def get_admin(admin_id):
    admin = Admin.objects.get(id=admin_id)
    return jsonify(admin)


@app.route('/api/v1/admin/get', methods=["GET"])
def get_all_admin():
    return jsonify(Admin.objects().all())


@app.route('/api/v1/admin/update', methods=["PUT"])
def update_admin():
    headers = request.headers
    data = request.get_json()

    if does_admin_exist(data["admin_id"]) is None:
        return Status.not_found()
    
    if (super_admin_check(headers["sender_id"])):
        admin = Admin.objects.get(id=data["admin_id"])
        setattr(admin, "access", data["access"])
        admin.save()
        return Status.updated()
    else:
        return Status.does_not_have_access()


@app.route('/api/v1/admin/delete/<admin_id>', methods=["DELETE"])
def delete_admin(admin_id):
    headers = request.headers

    if does_admin_exist(admin_id) is None:
        return Status.not_found()

    if super_admin_check(headers["sender_id"]):
        admin = Admin.objects.get(id=admin_id)
        admin.delete()
        return Status.deleted()
    
    else:
        return Status.does_not_have_access()
