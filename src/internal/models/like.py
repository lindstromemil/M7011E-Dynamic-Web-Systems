from mongoengine import Document, ReferenceField
from src.internal.models.rating import Rating
from src.internal.models.user import User


class Like(Document):
    user_id = ReferenceField(User)
    rating_id = ReferenceField(Rating)

    meta = {"collection": "likes"}
