from mongoengine import Document, StringField, ReferenceField
from src.internal.models.user import User


class Admin(Document):
    user_id = ReferenceField(User)
    access = StringField(required=True)

    meta = {"collection": "admins"}
