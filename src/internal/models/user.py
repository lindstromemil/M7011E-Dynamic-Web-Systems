from mongoengine import Document, StringField, DateTimeField, EmbeddedDocument, EmbeddedDocumentField


class UserProfile(EmbeddedDocument):
    image_path = StringField()
    description = StringField()
    settings = StringField()


class User(Document):
    username = StringField(unique=True, required=True)
    password = StringField(required=True)
    created_at = DateTimeField()
    profile = EmbeddedDocumentField(UserProfile)

    meta = {"collection": "users"}
