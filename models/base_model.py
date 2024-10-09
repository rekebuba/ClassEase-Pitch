#!/usr/bin/python3

from datetime import datetime
import models
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import declared_attr
from ethiopian_date import EthiopianDateConverter
import uuid
import bcrypt
import random

Base = declarative_base()


class BaseModel:
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
        """Returns a string representation of the instance"""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """Updates the public instance attribute updated_at with the current datetime"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary containing all keys/values of __dict__ of the instance"""
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
        """delete the current instance from the storage"""
        models.storage.delete(self)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def hash_password(self, password):
        self.password = bcrypt.hashpw(password.encode(
            'utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def generate_id(self, role):
        """Function to generate a custom student ID based on the grade"""
        id = ''
        section = ''

        if role == 'Student':
            section = 'MAS'
        elif role == 'Teacher':
            section = 'MAT'
        elif role == 'Admin':
            section = 'MAA'

        from models.student import Student
        from models.admin import Admin
        from models.teacher import Teacher

        role_class_map = {
            'Teacher': Teacher,
            'Student': Student,
            'Admin': Admin
        }

        unique = True
        while unique:
            num = random.randint(1000, 9999)
            starting_year = EthiopianDateConverter.date_to_ethiopian(
                datetime.now()).year % 100
            id = f'{section}/{num}/{starting_year}'
            if not self.id_exists(id, role_class_map[role]):
                unique = False
        return id

    def id_exists(self, id, role):
        """Function to check if the ID already exists"""
        from models import storage
        if storage.get_first(role, id=id):
            return True
        return False
