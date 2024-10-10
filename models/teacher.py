#!/usr/bin/python3

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.engine.db_storage import BaseModel, Base

class Teacher(BaseModel, Base):
    __tablename__ = 'teacher'
    id = Column(String(120), ForeignKey('users.id'), primary_key=True, unique=True)
    name = Column(String(50), nullable=False)
    email = Column(String(120), nullable=False)

    subject = relationship("Subject", backref="teacher", cascade="save-update", passive_deletes=True)
    section = relationship("Section", backref="teacher", cascade="save-update", passive_deletes=True)
    mark_list = relationship("MarkList", backref="teacher", cascade="save-update", passive_deletes=True)


    def __init__(self, *args, **kwargs):
        """initializes score"""
        super().__init__(*args, **kwargs)
