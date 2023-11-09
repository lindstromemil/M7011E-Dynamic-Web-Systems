
# Python Imports
import os

from src.internal import app


def _run():
    routes = []

    for rule in app.url_map.iter_rules():
        routes.append('%s' % rule)


    """ Imports the app and runs it. """
    print(routes)
    app.run()


if __name__ == '__main__':
    _run()