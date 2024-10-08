#!/usr/bin/python3
from models.engine.db_storage import DBStorage

storage = DBStorage()

def init_app(app):
    """ Initialize the storage with the Flask app """
    storage.init_app(app)
