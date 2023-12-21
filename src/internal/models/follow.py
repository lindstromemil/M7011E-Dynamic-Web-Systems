from mongoengine import Document, ReferenceField

from src.internal.models.user import User


class Followers(Document):
    user_id = ReferenceField(User)
    follower_id = ReferenceField(User)

    meta = {"collection": "followers"}


class Follows(Document):
    user_id = ReferenceField(User)
    followed_id = ReferenceField(User)

    meta = {"collection": "follows"}
