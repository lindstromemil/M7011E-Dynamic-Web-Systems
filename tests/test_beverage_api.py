import unittest
from src.internal.models.beverage import Beverage
from src.internal.models.user import User
from src.internal.models.admin import Admin
from src.internal import app

class TestBeverage(unittest.TestCase):
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
        admin = User(username="admin_user", password="admin")
        admin.save()
    
    def test_create_beverage_success(self):
        data = {
            "name": "Create Success",
            "description":"This is a new beverage",
            "image_path":"image.jpg",
            "bitterness":"1",
            "fullness":"1",
            "sweetness":"1",
            "abv":"1",
            "beverageType":"1",
            "country":"sweden",
            "brand_id":"Spendrups"
        }
        response = self.app.post("/api/v1/users/beverages", json=data)
        self.assertEqual(response.status_code, 201)


    def test_create_existing_beverage(self):
        data = {
            "name": "Create Fail",
            "description":"This is a new beverage",
            "image_path":"image.jpg",
            "bitterness":"1",
            "fullness":"1",
            "sweetness":"1",
            "abv":"1",
            "beverageType":"1",
            "country":"sweden",
            "brand_id":"Spendrups"
        }
        response_success = self.app.post("/api/v1/users/beverages", json=data)
        self.assertEqual(response_success.status_code, 201)
        response_fail = self.app.post("/api/v1/users/beverages", json=data)
        self.assertEqual(response_fail.status_code, 400)


    def get_beverage_success(self):
        data = {
            "name": "Get Success",
            "description":"This is a new beverage",
            "image_path":"image.jpg",
            "bitterness":"1",
            "fullness":"1",
            "sweetness":"1",
            "abv":"1",
            "beverageType":"1",
            "country":"sweden",
            "brand_id":"Spendrups"
        }
        response_create = self.app.post("/api/v1/users/beverages", json=data)
        self.assertEqual(response_create.status_code, 201)

        response_get = self.app.get("/api/v1/users/beverages")

    def test_beverage_cleanup(self):
        Beverage.objects(name="Create Success").delete()
        Beverage.objects(name="Create Fail").delete()
        Beverage.objects(name="Get Success").delete()
        pass