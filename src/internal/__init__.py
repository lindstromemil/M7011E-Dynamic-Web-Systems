import flask
from flask_mongoengine import MongoEngine
import src.internal.database.importDB as importDB
from flask_cors import CORS

from flask_jwt_extended import JWTManager
from datetime import timedelta

db = MongoEngine()
app = flask.Flask("m7011e_app")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["MONGODB_SETTINGS"] = [
    {
        "db": "m7011e",
        "host": "localhost",
        "port": 27017,
        "alias": "default",
    }
]

app.config["JWT_SECRET_KEY"] = "e8ea104a090c14ce12181b347a62ca5db09c2135e6403e40293123c2755bbb6fedcdd5f6b9eb89664b087c8"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=100)
jwt = JWTManager(app)

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
