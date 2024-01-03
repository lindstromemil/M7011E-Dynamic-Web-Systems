from mongoengine import Document, ReferenceField

from src.internal.models.beverage import Beverage
from src.internal.models.user import User


class Planning(Document):
    user_id = ReferenceField(User)
    beverage_id = ReferenceField(Beverage)

    meta = {"collection": "planning"}
