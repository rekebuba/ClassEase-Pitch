#!/usr/bin/python3

from sqlalchemy import create_engine
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_sqlalchemy import SQLAlchemy
from models.base_model import Base, BaseModel
from models.grade import Grade, seed_grades
from models.users import User
from models.student import Student
from models.section import Section
from models.admin import Admin
from models.subject import Subject
from models.teacher import Teacher
from models.assessment import Assessment
from models.mark_list import MarkList
from models.average_result import AVRGResult
from models.stud_yearly_record import StudentYearlyRecord
from models.teacher_record import TeachersRecord


class DBStorage:
    __engine = None

    def __init__(self):
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
            # Create tables using Base's metadata
            Base.metadata.create_all(bind=self.__engine.engine)

            # Create a session and seed grades after tables are created
            with self.__engine.session.begin():
                seed_grades(self.__engine.session)

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

    def drop_all(self):
        """Drop all tables."""
        with self.__engine.engine.begin() as conn:
            Base.metadata.drop_all(bind=conn)

    def rollback(self):
        """Rollback all changes."""
        self.get_session().rollback()

    def get_first(self, cls, **data):
        return self.get_session().query(cls).filter_by(**data).first()

    def get_all(self, cls, **data):
        return self.get_session().query(cls).filter_by(**data).all()

    def get_random(self, cls, **data):
        return self.get_session().query(cls).filter_by(**data).order_by(func.random()).first()
