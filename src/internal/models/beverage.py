from mongoengine import Document, StringField, ReferenceField, FloatField
from src.internal.models.brand import Brand


class Beverage(Document):
    name = StringField()
    description = StringField()
    image_path = StringField()
    bitterness = FloatField()
    fullness = FloatField()
    sweetness = FloatField()
    abv = FloatField()
    beverageType = StringField()
    country = StringField()
    brand_id = ReferenceField(Brand)

    meta = {"collection": "beverages"}
