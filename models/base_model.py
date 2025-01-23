#!/usr/bin/python3
""" Module for BaseModel class """

from datetime import datetime
import models
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, declared_attr, DeclarativeMeta
import uuid
import bcrypt
from typing import Type

Base: Type = declarative_base() # Base class for all models


class BaseModel:
    """
    BaseModel class

    Defines a base model for other classes to inherit from, providing common attributes and methods.

    Attributes:
        id (str): Primary key, a unique identifier for each instance.
        created_at (datetime): Timestamp when the instance was created.
        updated_at (datetime): Timestamp when the instance was last updated.

    Methods:
        __init__(*args, **kwargs): Initializes the instance with given attributes.
        __str__(): Returns a string representation of the instance.
        save(): Updates the updated_at attribute and saves the instance to storage.
        to_dict(): Returns a dictionary representation of the instance.
        delete(): Deletes the instance from storage.
        __tablename__(cls): Returns the table name for the class.
        hash_password(password): Hashes the given password and stores it.
        check_password(password): Checks if the given password matches the stored hashed password.
    """
    """Defines all common attributes/methods for other classes"""

    id = Column(String(120), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initializes the instance"""
        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                if key != '__class__':
                    setattr(self, key, value)
            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())
            if 'created_at' not in kwargs:
                self.created_at = datetime.utcnow()
            if 'updated_at' not in kwargs:
                self.updated_at = datetime.utcnow()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __str__(self):
        """
        Returns a string representation of the instance.

        The string representation includes the class name, the instance ID, 
        and the dictionary of the instance's attributes.

        Returns:
            str: A string in the format "[ClassName] (id) {attributes}".
        """
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """
        Saves the current instance to the storage.

        This method updates the `updated_at` attribute with the current UTC datetime,
        adds the instance to the storage, and then saves the storage.

        Returns:
            None
        """
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
        Converts the instance to a dictionary representation.

        This method creates a copy of the instance's `__dict__` attribute,
        removes any SQLAlchemy instance state and password fields if present,
        and adds the class name, creation time, and update time in ISO format.

        Returns:
            dict: A dictionary containing the instance's data.
        """
        new_dict = self.__dict__.copy()
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        if "password" in new_dict:
            del new_dict["password"]
        new_dict['__class__'] = self.__class__.__name__
        new_dict['created_at'] = self.created_at.isoformat()
        new_dict['updated_at'] = self.updated_at.isoformat()
        return new_dict

    def delete(self):
        """
        Delete the current instance from the storage.

        Raises:
            StorageError: If there is an issue with the storage system during deletion.
        """
        """delete the current instance from the storage"""
        models.storage.delete(self)

    @declared_attr
    def __tablename__(cls):
        """
        Returns the table name for the SQLAlchemy model.

        The table name is derived from the class name, converted to lowercase.

        Returns:
            str: The table name in lowercase.
        """
        return cls.__name__.lower()

    def hash_password(self, password):
        """
        Hashes a given password using bcrypt and stores the hashed password.

        Args:
            password (str): The plaintext password to be hashed.

        Returns:
            None
        """
        self.password = bcrypt.hashpw(password.encode(
            'utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        """
        Check if the provided password matches the stored hashed password.

        Args:
            password (str): The plaintext password to check.

        Returns:
            bool: True if the password matches the stored hashed password, False otherwise.
        """
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
