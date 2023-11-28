# Python imports

# Framework imports
from flask import jsonify

from src.internal import app
from src.internal.models.user import User, UserProfile
from src.internal.models.admin import Admin


@app.route("/", methods=["GET"])
def home():
    return "<p> Hello world! </p>"
