import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    # General secret key for the application
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Secret Keys for different roles
    ADMIN_SECRET_KEY = os.getenv("ADMIN_JWT_SECRET")
    TEACHER_SECRET_KEY = os.getenv("TEACHER_JWT_SECRET")
    STUDENT_SECRET_KEY = os.getenv("STUDENT_JWT_SECRET")

    # File upload configuration
    UPLOAD_FOLDER = "uploads"


class DevelopmentConfig(Config):
    user = os.getenv("KEY_MYSQL_USER")
    password = os.getenv("KEY_MYSQL_PWD")
    host = os.getenv("KEY_MYSQL_HOST")
    db = os.getenv("KEY_MYSQL_DB")
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"mysql://{user}:{password}@{host}/{db}"


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    DEBUG = True
    user = os.getenv("TEST_MYSQL_USER")
    password = os.getenv("TEST_MYSQL_PWD")
    host = os.getenv("TEST_MYSQL_HOST")
    db = os.getenv("TEST_MYSQL_DB")
    SQLALCHEMY_DATABASE_URI = f"mysql://{user}:{password}@{host}/{db}"
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///test_db'  # Using SQLite for testing
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Overriding the JWT secret keys for testing
    ADMIN_SECRET_KEY = os.getenv("TEST_ADMIN_JWT_SECRET")
    TEACHER_SECRET_KEY = os.getenv("TEST_TEACHER_JWT_SECRET")
    STUDENT_SECRET_KEY = os.getenv("TEST_STUDENT_JWT_SECRET")
