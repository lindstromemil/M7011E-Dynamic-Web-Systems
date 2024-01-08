from src.internal import app


@app.route("/", methods=["GET"])
def home():
    return "<p> Hello world! </p>"
