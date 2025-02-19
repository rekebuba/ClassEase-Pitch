#!/usr/bin/python3
"""This module initializes the storage system for ClassEase"""
from models.engine.db_storage import DBStorage

storage = DBStorage()

def init_app(app):
    """
    Initialize the storage with the Flask app.

    This function sets up the storage system to work with the provided Flask application instance.

    Args:
        app (Flask): The Flask application instance to initialize the storage with.
    """
    storage.init_app(app)
