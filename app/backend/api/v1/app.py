#!/usr/bin/python3
"""Main module for the API"""

from flask import jsonify
from api import create_app
from models.engine.db_storage import DBStorage
from models import storage

app = create_app('development')

@app.teardown_appcontext
def cleanup_session(exception=None):
    storage.session.remove()  # Clean up session after request


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    app.run(host=host, port=port, debug=True)
