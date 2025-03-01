#!/usr/bin/python3
"""This module defines a class to manage the database storage for ClassEase"""

from sqlalchemy.sql.expression import func
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_sqlalchemy import SQLAlchemy
from models.base_model import Base, BaseModel
from models.grade import Grade, seed_grades
from models.user import User
from models.student import Student
from models.section import Section
from models.admin import Admin
from models.subject import Subject
from models.teacher import Teacher
from models.assessment import Assessment
from models.mark_list import MarkList
from models.average_result import AVRGResult
from models.average_subject import AVRGSubject
from models.stud_yearly_record import StudentYearlyRecord
from models.teacher_record import TeachersRecord
from models.blacklist_token import BlacklistToken
from models.event import Event
from models.semester import Semester
from datetime import datetime


class DBStorage:
    """
    DBStorage is a class that provides an interface for interacting with a SQLAlchemy database.

    Attributes:
        __engine (SQLAlchemy): The SQLAlchemy engine instance.

    Methods:
        __init__():
        session:
        new(obj):
        init_app(app):
        close():
        add(obj):
        delete(obj=None):
        all(cls=None):
        save():
        drop_all():
        rollback():
        get_first(cls, **data):
        get_all(cls, **data):
        get_random(cls, **data):
    """
    __engine = None

    def __init__(self):
        """
        Initializes a new instance of the database storage engine.

        This method sets up the SQLAlchemy engine for database interactions.
        """
        self.__engine = SQLAlchemy()

    @property
    def session(self):
        """
        Retrieves the current database session.

        Returns:
            Session: The current database session.
        """
        return self.__engine.session

    def begin(self):
        return self.__engine.session.begin()

    def new(self, obj):
        """
        Add the object to the current database session.

        Args:
            obj: The object to be added to the session.
        """
        """add the object to the current database session"""
        self.session.add(obj)

    def init_app(self, app):
        """
        Initialize the database with the Flask app.

        This method sets up the database engine with the provided Flask application,
        creates all tables defined in the Base metadata, and seeds the grades table.

        Args:
            app (Flask): The Flask application instance to initialize the database with.
        """
        self.__engine.init_app(app)
        with app.app_context():
            # Create tables using Base's metadata
            Base.metadata.create_all(bind=self.__engine.engine)

            with self.session.begin():
                seed_grades(self.session)

    def close(self):
        """
        Closes the current session by removing it from the session registry.
        This ensures that the session is properly cleaned up and resources are released.
        """
        self.session.remove()

    def add(self, obj):
        """
        Add an object to the current database session and commit the transaction.

        Args:
            obj: The object to be added to the session.
        """
        self.session.add(obj)

    def delete(self, obj=None):
        """
        Deletes the specified object from the current database session.

        Args:
            obj: The object to be deleted from the database session. If None, no action is taken.
        """
        if obj is not None:
            self.session.delete(obj)

    def all(self, cls=None):
        """
        Query on the current database session.

        Args:
            cls (type, optional): The class to query. If provided, the method will
                                  return all instances of this class from the database.

        Returns:
            list: A list of all instances of the specified class if `cls` is provided.
                  If `cls` is None, the method returns None.
        """
        if cls is not None:
            return self.session.query(cls).all()
        return

    def save(self):
        """
        Commit all changes of the current database session.

        This method commits any pending transactions to the database, ensuring that all changes made
        during the current session are saved.
        """
        self.session.commit()

    def drop_all(self):
        """
        Drop all tables in the database.

        This method uses the SQLAlchemy engine to drop all tables defined in the
        metadata. It ensures that the operation is performed within a transaction
        context to maintain database integrity.

        Raises:
            SQLAlchemyError: If there is an error during the drop operation.
        """
        with self.__engine.engine.begin() as conn:
            Base.metadata.drop_all(bind=conn)

    def rollback(self):
        """
        Rollback all changes made in the current session.

        This method reverts all uncommitted changes made to the database
        in the current session, ensuring that the database state is 
        consistent with the last committed state.
        """
        self.session.rollback()

    def get_first(self, cls, **data):
        """
        Retrieve the first record that matches the given criteria.

        Args:
            cls (Type): The class of the table to query.
            **data: Arbitrary keyword arguments representing the filter criteria.

        Returns:
            object: The first record that matches the given criteria, or None if no match is found.
        """
        return self.session.query(cls).filter_by(**data).first()

    def get_all(self, cls, **data):
        """
        Retrieve all records of a given class that match the specified filter criteria.

        Args:
            cls (Type): The class of the records to retrieve.
            **data: Arbitrary keyword arguments representing the filter criteria.

        Returns:
            List: A list of all records that match the filter criteria.
        """
        return self.session.query(cls).filter_by(**data).all()

    def get_random(self, cls, **data):
        """
        Retrieve a random record from the database that matches the given criteria.

        Args:
            cls (Type): The class of the database model to query.
            **data: Arbitrary keyword arguments representing the filter criteria.

        Returns:
            An instance of `cls` that matches the filter criteria, selected randomly.
            If no matching record is found, returns None.
        """
        return self.session.query(cls).filter_by(**data).order_by(func.random()).first()
