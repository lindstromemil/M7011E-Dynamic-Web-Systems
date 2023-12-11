from mongoengine import Document, StringField, ReferenceField, FloatField
from src.internal.models.brand import Brand


class Beverage(Document):
    name = StringField(required=True)
    description = StringField(required=True)
    image_path = StringField(required=True)
    bitterness = FloatField(required=True)
    fullness = FloatField(required=True)
    sweetness = FloatField(required=True)
    abv = FloatField(required=True)
    beverageType = StringField(required=True)
    country = StringField(required=True)
    brand_id = ReferenceField(Brand)

    meta = {"collection": "beverages"}
