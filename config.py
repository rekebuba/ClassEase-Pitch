import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")  # General secret key for the application
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Secret Keys for different roles
    ADMIN_SECRET_KEY = os.getenv("ADMIN_JWT_SECRET")
    TEACHER_SECRET_KEY = os.getenv("TEACHER_JWT_SECRET")
    STUDENT_SECRET_KEY = os.getenv("STUDENT_JWT_SECRET")

class DevelopmentConfig(Config):
    user = os.getenv('KEY_MYSQL_USER')
    password = os.getenv('KEY_MYSQL_PWD')
    host = os.getenv('KEY_MYSQL_HOST')
    db = os.getenv('KEY_MYSQL_DB')
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'mysql://{user}:{password}@{host}/{db}'

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'  # Using SQLite for testing
