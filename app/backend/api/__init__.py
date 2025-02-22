import os
from flask import Flask
from flask_cors import CORS
from models import storage


def create_app(config_name):
    """
    Create a Flask application.

    Args:
        config_name (str): The configuration name. It can be 'testing', 'development', or any other value for production.

    Returns:
        Flask: The Flask application instance.

    The function performs the following tasks:
    - Initializes the Flask application.
    - Loads the appropriate configuration based on the provided config_name.
    - Initializes the database with the application context.
    - Enables Cross-Origin Resource Sharing (CORS) for the specified routes.
    - Imports and registers the necessary blueprints for different parts of the application.
    """
    """ Create a Flask application """
    base_dir = os.path.abspath(os.path.dirname(__file__))
    static_dir = os.path.join(base_dir, 'v1/static')
    app = Flask(__name__, static_folder=static_dir, static_url_path='/static')

    # Load configuration
    if config_name == 'testing':
        app.config.from_object('config.TestingConfig')
    elif config_name == 'development':
        app.config.from_object('config.DevelopmentConfig')
    else:
        app.config.from_object('config.ProductionConfig')

    # Initialize database
    storage.init_app(app)

    # Enable CORS
    CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

    # Import and register blueprints
    from api.v1.views.auth import auth
    from api.v1.views.admin import admin
    from api.v1.views.students import stud
    from api.v1.views.teachers import teach
    from api.v1.views.shared_access import shared

    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(stud)
    app.register_blueprint(teach)
    app.register_blueprint(shared)

    return app
