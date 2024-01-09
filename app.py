from src.internal import app
from src.internal.database import importDB


def _run():
    routes = []

    for rule in app.url_map.iter_rules():
        routes.append("%s" % rule)

    """ Imports the app and runs it. """
    print(routes)
    importDB.insert_db_from_csv()  # Import the database from CSV
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    _run()
