from mongoengine import DateTimeField, StringField, Document, FloatField, ReferenceField

from src.internal.models.beverage import Beverage
from src.internal.models.user import User


class Rating(Document):
    user_id = ReferenceField(User)
    beverage_id = ReferenceField(Beverage)
    score = FloatField()
    comment = StringField()
    created_at = DateTimeField()

    meta = {"collection": "ratings"}
