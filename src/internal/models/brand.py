from mongoengine import Document, StringField


class Brand(Document):
    name = StringField(unique=True, required=True)
    description = StringField()

    meta = {"collection": "brands"}
