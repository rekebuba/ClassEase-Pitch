#!/usr/bin/python3

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.engine.db_storage import BaseModel, Base


class Teacher(BaseModel, Base):
    __tablename__ = 'teacher'
    id = Column(String(120), ForeignKey('users.id'),
                primary_key=True, unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    gender = Column(String(10), nullable=False)
    age = Column(String(20), nullable=False)
    email = Column(String(120), nullable=False)
    phone = Column(String(25), nullable=False)
    address = Column(String(120), nullable=False)
    experience = Column(Integer, nullable=False)
    qualification = Column(String(120), nullable=False)
    subject_taught = Column(String(120), nullable=False)
    no_of_mark_list = Column(Integer, nullable=True, default=0)

    
    def __init__(self, *args, **kwargs):
        """initializes score"""
        super().__init__(*args, **kwargs)
