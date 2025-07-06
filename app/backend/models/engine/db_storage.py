#!/usr/bin/python3
"""This module defines a class to manage the database storage for ClassEase"""

from typing import Any, List, Optional, Type, Union, overload
from sqlalchemy import create_engine, Engine
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from flask import Flask
from api.v1.utils.typing import BaseT
from models.base_model import Base
from models.grade import Grade  # noqa: F401
from models.user import User  # noqa: F401
from models.student import Student  # noqa: F401
from models.section import Section  # noqa: F401
from models.admin import Admin  # noqa: F401
from models.subject import Subject  # noqa: F401
from models.teacher import Teacher  # noqa: F401
from models.assessment import Assessment  # noqa: F401
from models.mark_list import MarkList  # noqa: F401
from models.student_term_record import StudentTermRecord  # noqa: F401
from models.subject_yearly_average import SubjectYearlyAverage  # noqa: F401
from models.student_year_record import StudentYearRecord  # noqa: F401
from models.teacher_record import TeachersRecord  # noqa: F401
from models.blacklist_token import BlacklistToken  # noqa: F401
from models.event import Event  # noqa: F401
from models.academic_term import AcademicTerm  # noqa: F401
from models.saved_query_view import SavedQueryView  # noqa: F401
from models.year import Year  # noqa: F401
from models.stream import Stream  # noqa: F401
from models.table import Table, seed_table  # noqa: F401
from models.grade_stream_link import GradeStreamLink  # noqa: F401
from models.teacher_subject_link import TeacherSubjectLink  # noqa: F401
from models.teacher_grade_link import TeacherGradeLink  # noqa: F401
from models.teacher_yearly_subject_link import TeacherYearlySubjectLink  # noqa: F401
from models.teacher_record_section_link import TeacherRecordSectionLink  # noqa: F401
from models.yearly_subject import YearlySubject  # noqa: F401
from contextlib import contextmanager


class DBStorage:
    """
    DBStorage is a class that provides an interface for interacting with a SQLAlchemy database.

    Attributes:
        __engine (Engine): The SQLAlchemy engine instance.
        __session (scoped_session): The current database session.
        __session_factory (sessionmaker): Factory for creating new sessions.
    """

    __engine: Optional[Engine] = None
    __session: Optional[scoped_session[Session]] = None
    __session_factory: Optional[sessionmaker[Session]] = None

    def __init__(self) -> None:
        """
        Initializes the SQLAlchemy engine and session factory.
        """
        self.__engine = None
        self.__session_factory = None
        self.__session = None

    @property
    def session(self) -> scoped_session[Session]:
        """
        Retrieves the current database session.

        Returns:
            scoped_session: The current database session.

        Raises:
            RuntimeError: If session is not initialized.
        """
        if self.__session is None:
            raise RuntimeError("Session not initialized. Call init_app() first.")
        return self.__session

    @property
    def engine(self) -> Engine:
        """
        Retrieves the current database engine.

        Returns:
            Engine: The SQLAlchemy engine instance.

        Raises:
            RuntimeError: If engine is not initialized.
        """
        if self.__engine is None:
            raise RuntimeError("Engine not initialized. Call init_app() first.")
        return self.__engine

    @property
    def metadata(self) -> Any:
        """
        Retrieves the metadata for the database.

        Returns:
            Any: The metadata for the database.
        """
        return Base.metadata

    def create_scoped_session(self, **kwargs: Any) -> scoped_session[Session]:
        """
        Create a scoped session for the database.

        Args:
            **kwargs: Additional arguments to pass to `sessionmaker`.

        Returns:
            scoped_session: A new scoped session.

        Raises:
            RuntimeError: If engine is not initialized.
        """
        if self.__engine is None:
            raise RuntimeError("Engine not initialized. Call init_app() first.")
        session_factory = sessionmaker(bind=self.__engine, **kwargs)

        # return a scoped session
        return scoped_session(session_factory)

    @contextmanager
    def begin(self) -> Any:
        """
        Context manager for transaction management.

        Yields:
            Any: The transaction context.
        """
        with self.session.begin() as transaction:
            yield transaction

    def new(self, obj: Base) -> None:
        """
        Add the object to the current database session.

        Args:
            obj (Base): The object to be added to the session.
        """
        self.session.add(obj)

    def init_app(self, app: Flask) -> None:
        """
        Initialize the database with the Flask app.

        This method sets up the database engine with the provided Flask application,
        creates all tables defined in the Base metadata, and seeds the grades table.

        Args:
            app (Flask): The Flask application instance to initialize the database with.
        """
        # Configure the database engine
        self.__engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
        self.__session_factory = sessionmaker(bind=self.__engine)
        self.__session = scoped_session(self.__session_factory)

        # Create tables and seed data
        with app.app_context():
            self.metadata.create_all(bind=self.__engine)  # create all tables
            self.seed_data()

    def seed_data(self) -> None:
        """
        Seed initial data into the database.
        """
        seed_table(self.session, self.engine)

    def close(self) -> None:
        """
        Close the current session.
        """
        if self.__session:
            self.__session.remove()
            self.__session = None

    def add(self, obj: Base) -> None:
        """
        Add an object to the current database session and commit the transaction.

        Args:
            obj (Base): The object to be added to the session.
        """
        self.session.add(obj)

    def delete(self, obj: Optional[Base] = None) -> None:
        """
        Deletes the specified object from the current database session.

        Args:
            obj (Optional[Base]): The object to be deleted from the database session.
                                  If None, no action is taken.
        """
        if obj is not None:
            self.session.delete(obj)

    @overload
    def all(self, cls: Type[BaseT]) -> List[BaseT]: ...

    @overload
    def all(self, cls: None = None) -> List[Any]: ...

    def all(self, cls: Optional[Type[BaseT]] = None) -> Union[List[BaseT], List[Any]]:
        """
        Query on the current database session.

        Args:
            cls (Optional[Type[BaseT]]): The class to query. If provided, the method will
                                     return all instances of this class from the database.

        Returns:
            Union[List[BaseT], List[Any]]: A list of all instances of the specified class if `cls` is provided.
                                       If `cls` is None, the method returns an empty list.
        """
        if cls is not None:
            return self.session.query(cls).all()
        return []

    def save(self) -> None:
        """
        Commit all changes of the current database session.
        """
        self.session.commit()

    def drop_all(self) -> None:
        """
        Drop all tables in the database.

        Raises:
            SQLAlchemyError: If there is an error during the drop operation.
        """
        if self.__engine is not None:
            Base.metadata.drop_all(bind=self.__engine)

    def reflect(self) -> None:
        """
        Reflect the database tables.

        Raises:
            SQLAlchemyError: If there is an error during the reflection operation.
            RuntimeError: If engine is not initialized.
        """
        if self.__engine is None:
            raise RuntimeError("Engine not initialized. Call init_app() first.")
        Base.metadata.reflect(bind=self.__engine)

    def rollback(self) -> None:
        """
        Rollback all changes made in the current session.
        """
        self.session.rollback()

    def get_first(self, cls: Type[BaseT], **data: Any) -> Optional[BaseT]:
        """
        Retrieve the first record that matches the given criteria.

        Args:
            cls (Type[BaseT]): The class of the table to query.
            **data: Arbitrary keyword arguments representing the filter criteria.

        Returns:
            Optional[BaseT]: The first record that matches the criteria, or None if no match is found.
        """
        return self.session.query(cls).filter_by(**data).first()

    def get_all(self, cls: Type[BaseT], **data: Any) -> List[BaseT]:
        """
        Retrieve all records of a given class that match the specified filter criteria.

        Args:
            cls (Type[BaseT]): The class of the records to retrieve.
            **data: Arbitrary keyword arguments representing the filter criteria.

        Returns:
            List[BaseT]: A list of all records that match the filter criteria.
        """
        return self.session.query(cls).filter_by(**data).all()

    def get_random(self, cls: Type[BaseT], **data: Any) -> Optional[BaseT]:
        """
        Retrieve a random record from the database that matches the given criteria.

        Args:
            cls (Type[BaseT]): The class of the database model to query.
            **data: Arbitrary keyword arguments representing the filter criteria.

        Returns:
            Optional[BaseT]: A random record that matches the criteria, or None if no match is found.
        """
        return self.session.query(cls).filter_by(**data).order_by(func.random()).first()
