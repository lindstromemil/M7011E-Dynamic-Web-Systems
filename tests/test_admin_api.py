import unittest
from src.internal.models.admin import Admin
from src.internal.models.user import User
from src.internal import app


class TestAdmin(unittest.TestCase):  
    def setUp(self):
        app.config['TESTING'] = True
        app.config["MONGODB_SETTINGS"] = [
            {
                "db": "m7011e-test",
                "host": "localhost",
                "port": 27017,
                "alias": "default",
            }
        ]
        self.app = app.test_client()
        User.objects().delete()
        Admin.objects().delete()

        #Create test users
        user = User(username="normal_user", password="password")
        user.save()
        admin = User(username="admin_user", password="admin")
        admin.save()
        super_admin = User(username="super_admin_user", password="super_admin")
        super_admin.save()

        super_id = User.objects.get(username="super_admin_user").id
        response = self.app.post("/api/v1/admin/me", headers={"sender_id": super_id})
        self.assertEqual(response.status_code, 201)


    def test_create_admin_success(self):
        user_id = User.objects.get(username="admin_user").id
        super_admin_id = Admin.objects().first().user_id.id

        data = {"user_id": user_id, "access": "admin"}
        headers = {"sender_id": super_admin_id}

        response = self.app.post("/api/v1/admin/create", json=data, headers=headers)
        self.assertEqual(response.status_code, 201)


    def test_create_super_admin_fail(self):
        user_id = User.objects().get(username="normal_user").id

        data = {"user_id": user_id, "access": "admin",}
        headers = {"sender_id": user_id}

        response = self.app.post("/api/v1/admin/create", json=data, headers=headers)
        self.assertEqual(response.status_code, 403)


    def test_get_admin_success(self):
        admin_id = Admin.objects().first().user_id.id
        response = self.app.get("/api/v1/admin/get/"+str(admin_id))
        self.assertEqual(response.status_code, 200)


    def test_update_admin_success(self):
        name = "update_test_user"
        test_user = User(username=name,password="test_password")
        test_user.save()

        admin = Admin(user_id=test_user.id, access="admin")
        admin.save()

        data = {"admin_id": admin.user_id.id,"access": "super_admin"}
        headers = {"sender_id": Admin.objects().first().user_id.id}

        response = self.app.put("/api/v1/admin/update", json=data, headers=headers)
        self.assertEqual(response.status_code, 200)


    def test_delete_userr_success(self):
        super_admin_id = Admin.objects().first().user_id.id
        response = self.app.delete("/api/v1/admin/delete/" + str(super_admin_id), headers={"sender_id": super_admin_id})
        self.assertEqual(response.status_code, 200)


    def test_cleanup(self):
        User.objects().delete()
        Admin.objects().delete()
        pass
