#!/usr/bin/python3
"""This module defines a class to manage the database storage for ClassEase"""

from sqlalchemy import create_engine
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_sqlalchemy import SQLAlchemy
from models.base_model import Base
from models.grade import Grade, seed_grades
from models.user import User
from models.student import Student
from models.section import Section
from models.admin import Admin
from models.subject import Subject, seed_subjects
from models.teacher import Teacher
from models.assessment import Assessment
from models.mark_list import MarkList
from models.stud_semester_record import STUDSemesterRecord
from models.average_subject import AVRGSubject
from models.stud_year_record import STUDYearRecord
from models.teacher_record import TeachersRecord
from models.blacklist_token import BlacklistToken
from models.event import Event
from models.semester import Semester
from models.year import Year, seed_year
from models.stream import Stream, seed_streams
from datetime import datetime
from flask import current_app


class DBStorage:
    """
    DBStorage is a class that provides an interface for interacting with a SQLAlchemy database.

    Attributes:
        __engine (SQLAlchemy): The SQLAlchemy engine instance.
        __session (Session): The current database session.
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes the SQLAlchemy engine and session factory.
        """
        self.__engine = None
        self.__session_factory = None

    @property
    def session(self):
        """
        Retrieves the current database session.
        """
        if self.__session is None:
            raise RuntimeError(
                "Session not initialized. Call init_app() first.")
        return self.__session

    @property
    def engine(self):
        """
        Retrieves the current database engine.
        """
        if self.__engine is None:
            raise RuntimeError(
                "Engine not initialized. Call init_app() first.")
        return self.__engine

    @property
    def metadata(self):
        """
        Retrieves the metadata for the database.
        """
        return Base.metadata

    def create_scoped_session(self, **kwargs):
        """
            Create a scoped session for the database.

        Args:
            **kwargs: Additional arguments to pass to `sessionmaker`.
        """
        if self.__engine is None:
            raise RuntimeError(
                "Engine not initialized. Call init_app() first.")
        session_factory = sessionmaker(bind=self.__engine, **kwargs)

        # return a scoped session
        return scoped_session(session_factory)

    def begin(self):
        return self.session.begin()

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
        # Configure the database engine
        self.__engine = create_engine(
            app.config['SQLALCHEMY_DATABASE_URI'])
        self.__session_factory = sessionmaker(bind=self.__engine)
        self.__session = scoped_session(self.__session_factory)

        # Create tables and seed data
        with app.app_context():
            self.metadata.create_all(bind=self.__engine)  # create all tables
            self.seed_data()

    def seed_data(self):
        """Seed initial data into the database."""
        # with self.session.begin():
        seed_grades(self.session)
        seed_streams(self.session)
        seed_subjects(self.session)
        seed_year(self.session)

    def close(self):
        """Close the current session."""
        if self.__session:
            self.__session.remove()
            self.__session = None

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
                  If `cls` is None, the method returns [].
        """
        if cls is not None:
            return self.session.query(cls).all()
        return []

    def save(self):
        """Commit all changes of the current database session."""
        self.session.commit()

    def drop_all(self):
        """
        Drop all tables in the database.

        Raises:
            SQLAlchemyError: If there is an error during the drop operation.
        """
        Base.metadata.drop_all(bind=self.__engine)

    def reflect(self):
        """
        Reflect the database tables.

        Raises:
            SQLAlchemyError: If there is an error during the reflection operation.
        """
        Base.metadata.reflect(bind=self.__engine)

    def rollback(self):
        """Rollback all changes made in the current session."""
        self.session.rollback()

    def get_first(self, cls, **data):
        """
        Retrieve the first record that matches the given criteria.

        Args:
            cls (Type): The class of the table to query.
            **data: Arbitrary keyword arguments representing the filter criteria.
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
        """
        return self.session.query(cls).filter_by(**data).order_by(func.random()).first()
