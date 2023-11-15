from mongoengine import Document, StringField


class Beverage(Document):
    name = StringField()
    description = StringField()
    image_path = StringField()

    meta = {"collection": "beverages"}
