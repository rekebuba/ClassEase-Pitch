#!/usr/bin/python3
""" Module for Average Result class """

from sqlalchemy import Column, String, Integer, ForeignKey, Float
from models.engine.db_storage import BaseModel, Base


class AVRGSubject(BaseModel, Base):
    __tablename__ = 'average_subject'
    user_id = Column(String(120), ForeignKey('users.id'), nullable=False)
    subject_id = Column(String(120), ForeignKey('subjects.id'), nullable=False)
    year_record_id = Column(String(120), ForeignKey(
        'student_year_records.id'), nullable=True)
    teachers_record_id = Column(String(120), ForeignKey(
        'teachers_record.id', ondelete="SET NULL"), nullable=True, default=None)
    # The actual average score of the student in this for all subject
    average = Column(Float, default=None)
    rank = Column(Integer, default=None)

    def __init__(self, *args, **kwargs):
        """initializes score"""
        super().__init__(*args, **kwargs)
