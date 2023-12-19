import unittest
from src.internal.models.user import User
from src.internal import app


class TestUser(unittest.TestCase):
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


    def test_create_user_success(self):
        data = {
            "username": "test_user",
            "password": "test_password",
            "image_path": "/path/to/image",
            "description": "Test description"
        }

        response = self.app.post("/api/v1/users/create", json=data)
        self.assertEqual(response.status_code, 201)


    def test_create_user_username_already_in_use(self):
        data = {
            "username": "create_test_user",
            "password": "test_password",
            "image_path": "/path/to/image",
            "description": "Test description"
        }
        response1 = self.app.post("/api/v1/users/create", json=data)
        self.assertEqual(response1.status_code, 201)
        response2 = self.app.post("/api/v1/users/create", json=data)
        self.assertEqual(response2.status_code, 400)



    def test_get_user_success(self):
        name = "get_test_user"
        test_user = User(username=name,password="test_password")
        test_user.save()

        response = self.app.get("/api/v1/users/get/" + name)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.content_type, 'application/json')
        json_data = response.get_json()
        self.assertEqual(json_data["username"], name)
        self.assertEqual(json_data["password"], "test_password")


    def test_update_user_success(self):
        name = "update_test_user"
        test_user = User(username=name,password="test_password")
        test_user.save()

        user_id = User.objects.get(username=name).id
        data = {"id": user_id,"password": "123"}
        headers = {"sender_id": user_id}

        response = self.app.put("/api/v1/users/update", json=data, headers=headers)
        self.assertEqual(response.status_code, 200)


    def test_delete_userr_success(self):
        name = "delete_test_user"
        test_user = User(username=name,password="test_password")
        test_user.save()

        user_id = User.objects.get(username=name).id
        headers = {"sender_id": user_id}

        response = self.app.delete("/api/v1/users/delete/" + name, headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_cleanup(self):
        User.objects().delete()
        pass


if __name__ == '__main__':
    unittest.main()