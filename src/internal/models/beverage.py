from mongoengine import Document, StringField, ReferenceField
from src.internal.models.brand import Brand


class Beverage(Document):
    name = StringField()
    description = StringField()
    image_path = StringField()
    brewery_id = ReferenceField(Brand)

    meta = {"collection": "beverages"}
