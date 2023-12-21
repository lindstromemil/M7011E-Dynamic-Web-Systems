import unittest
from src.internal.models.follow import Followers, Follows
from src.internal.models.user import User
from src.internal import app


class TesTFollow(unittest.TestCase):  
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

        #Create 2 test users
        u1 = User(username="first", password="password")
        u1.save()

        u2 = User(username="second", password="password")
        u2.save()


    def test_create_follow_success(self):
        u1 = User.objects.get(username="first")
        u2 = User.objects.get(username="second")

        data = {"user_id": u1.id, "target_id": u2.id}
        headers = {"sender_id": u1.id}

        response = self.app.post("/api/v1/follow/create", json=data, headers=headers)
        self.assertEqual(response.status_code, 201)


    def test_delete_follow_success(self):
        u1 = User.objects.get(username="first").id
        u2 = User.objects.get(username="second").id

        follow = Follows(user_id=u1, followed_id=u2)
        followBy = Followers(user_id=u2, follower_id=u1)
        follow.save()
        followBy.save()

        data = {"user_id": u1, "target_id": u2}
        headers = {"sender_id": u1}

        response = self.app.delete("/api/v1/follow/delete", json=data, headers=headers)
        self.assertEqual(response.status_code, 200)

