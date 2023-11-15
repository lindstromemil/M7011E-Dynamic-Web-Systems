from mongoengine import DateTimeField, Document, IntField, ReferenceField

from src.internal.models.beverage import Beverage
from src.internal.models.user import User


class Rating(Document):
    user_id = ReferenceField(User)
    beer_id = ReferenceField(Beverage)
    score = IntField()
    created_at = DateTimeField()

    meta = {"collection": "ratings"}
