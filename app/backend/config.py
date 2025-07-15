import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    # General secret key for the application
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Secret Keys for different roles
    CEO_SECRET_KEY = os.getenv("CEO_JWT_SECRET")
    ADMIN_SECRET_KEY = os.getenv("ADMIN_JWT_SECRET")
    TEACHER_SECRET_KEY = os.getenv("TEACHER_JWT_SECRET")
    STUDENT_SECRET_KEY = os.getenv("STUDENT_JWT_SECRET")

    # File upload configuration
    UPLOAD_FOLDER = "uploads"

    secret_id = os.getenv("SECRET_ID")


class DevelopmentConfig(Config):
    DEBUG = True

    @staticmethod
    def init_app(app):
        user = os.getenv("DEV_MYSQL_USER")
        password = os.getenv("DEV_MYSQL_PWD")
        host = os.getenv("DB_HOST", "localhost")
        db = os.getenv("DEV_MYSQL_DB")
        if not all([user, password, host, db]):
            raise ValueError("Missing required environment variables for db connection")

        app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{user}:{password}@{host}/{db}"


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    DEBUG = True

    @staticmethod
    def init_app(app):
        user = os.getenv("TEST_MYSQL_USER")
        password = os.getenv("TEST_MYSQL_PWD")
        host = os.getenv("DB_HOST", "localhost")

        db = os.getenv("TEST_MYSQL_DB")

        if not all([user, password, host, db]):
            raise ValueError("Missing required environment variables for db connection")

        app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{user}:{password}@{host}/{db}"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        # Overriding the JWT secret keys for testing
        app.config["CEO_SECRET_KEY"] = os.getenv("TEST_CEO_JWT_SECRET")
        app.config["ADMIN_SECRET_KEY"] = os.getenv("TEST_ADMIN_JWT_SECRET")
        app.config["TEACHER_SECRET_KEY"] = os.getenv("TEST_TEACHER_JWT_SECRET")
        app.config["STUDENT_SECRET_KEY"] = os.getenv("TEST_STUDENT_JWT_SECRET")
