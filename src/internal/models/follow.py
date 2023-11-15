from mongoengine import Document, ReferenceField

from src.internal.models.user import User


class FollowedBy(Document):
    user_id = ReferenceField(User)
    follower_id = ReferenceField(User)

    meta = {"collection": "followed_by"}


class Follows(Document):
    user_id = ReferenceField(User)
    followed_id = ReferenceField(User)

    meta = {"collection": "follows"}
