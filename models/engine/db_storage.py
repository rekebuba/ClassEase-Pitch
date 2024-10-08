#!/usr/bin/python3

from sqlalchemy import create_engine
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_sqlalchemy import SQLAlchemy
from models.base_model import Base, BaseModel
from models.grade import Grade
from models.student import Student
from models.section import Section
# from models.users import User
from models.admin import Admin
from models.subject import Subject
from models.teacher import Teacher
from models.assessment import Assessment
from models.mark_list import MarkList


class DBStorage:
    __engine = None
    # get_session() = None

    def __init__(self):
        # Retrieve environment variables
        # user = os.getenv('KEY_MYSQL_USER')
        # password = os.getenv('KEY_MYSQL_PWD')
        # host = os.getenv('KEY_MYSQL_HOST')
        # db = os.getenv('KEY_MYSQL_DB')
        
        # # Create engine
        # self.__engine = create_engine(f'mysql+mysqldb://{user}:{password}@{host}/{db}')
        self.__engine = SQLAlchemy()

    def get_session(self):
        return self.__engine.session

    def new(self, obj):
        """add the object to the current database session"""
        self.get_session().add(obj)

    def init_app(self, app):
        """Initialize the database with the Flask app."""
        self.__engine.init_app(app)
        with app.app_context():
            Base.metadata.create_all(bind=self.__engine.engine)  # Create tables using Base's metadata


    # def reload(self):
    #     Base.metadata.create_all(self.__engine)
    #     session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
    #     Session = scoped_session(session_factory)
    #     self.get_session() = Session()

    def close(self):
        self.get_session().remove()

    # Add methods to create, retrieve, update, and delete records
    def add(self, obj):
        session = self.get_session()  # Get the current session
        session.add(obj)
        session.commit()  

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.get_session().delete(obj)

    def all(self, cls=None):
        """query on the current database session"""
        if cls is not None:
            return self.get_session().query(cls).all()
        return

    def save(self):
        """commit all changes of the current database session"""
        self.__engine.session.commit()
        # self.get_session().commit()

    # def get(self, cls, id):
    #     user = self.get_session().query(cls).filter(cls.id == id).one_or_none()
    #     return user.to_dict()

    def get_first(self, cls, **data):
        return self.get_session().query(cls).filter_by(**data).first()

    def get_all(self, cls, **data):
        return self.get_session().query(cls).filter_by(**data).all()

    def get_random(self, cls, **data):
        return self.get_session().query(cls).filter_by(**data).order_by(func.rand()).first()
