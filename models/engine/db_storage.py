#!/usr/bin/python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base, BaseModel
from models.grades import Grade
from models.student import Student
from models.section import Section
from models.users import User
# from models.grades import Grade
import os


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        # Retrieve environment variables
        user = os.getenv('KEY_MYSQL_USER')
        password = os.getenv('KEY_MYSQL_PWD')
        host = os.getenv('KEY_MYSQL_HOST')
        db = os.getenv('KEY_MYSQL_DB')
        
        # Create engine
        self.__engine = create_engine(f'mysql+mysqldb://{user}:{password}@{host}/{db}')

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        self.__session.remove()

    # Add methods to create, retrieve, update, and delete records
    def add(self, obj):
        self.__session.add(obj)
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def all(self, cls=None):
        """query on the current database session"""
        if cls is not None:
            return self.__session.query(cls).all()
        return

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def get(self, cls, id):
        user = self.__session.query(cls).filter(cls.id == id).one_or_none()
        print(user.to_dict())
        return user.to_dict()
