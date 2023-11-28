from mongoengine import Document, StringField


class Brand(Document):
    name = StringField()
    description = StringField()

    meta = {"collection": "brands"}
