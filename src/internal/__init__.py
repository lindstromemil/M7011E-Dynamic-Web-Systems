import flask
from flask_mongoengine import MongoEngine

db = MongoEngine()
app = flask.Flask("m7011e_app")
app.config["MONGODB_SETTINGS"] = [
    {
        "db": "m7011e",
        "host": "localhost",
        "port": 27017,
        "alias": "default",
    }
]

db.init_app(app)

import src.internal.api.user_api
import src.internal.api.ratings_api
import src.internal.api.planning_api
import src.internal.api.likes_api
import src.internal.api.admin_api
import src.internal.api.follow_api
import src.internal.api.beverage_api
import src.internal.api.brand_api
import src.internal.api.api
