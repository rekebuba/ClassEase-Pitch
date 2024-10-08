from flask import Flask
from models import storage
from models import init_app

def create_app(config_name):
    app = Flask(__name__)
    
    # Load configuration
    if config_name == 'testing':
        app.config.from_object('config.TestingConfig')
    elif config_name == 'development':
        app.config.from_object('config.DevelopmentConfig')
    else:
        app.config.from_object('config.ProductionConfig')

    # Initialize database
    storage.init_app(app)

    # Import and register blueprints
    from api.v1.views.admin import auth
    from api.v1.views.students import stud
    from api.v1.views.teachers import teach
    from api.v1.views.public import app_views

    app.register_blueprint(stud)
    app.register_blueprint(auth)
    app.register_blueprint(teach)
    app.register_blueprint(app_views)

    return app
