from mongoengine import Document, StringField, DateTimeField, EmbeddedDocument, EmbeddedDocumentField


class UserProfile(EmbeddedDocument):
    image_path = StringField()
    description = StringField()
    settings = StringField()


class User(Document):
    username = StringField()
    password = StringField()
    created_at = DateTimeField()
    profile = EmbeddedDocumentField(UserProfile)

    meta = {"collection": "users"}
