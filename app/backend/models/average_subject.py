#!/usr/bin/python3
""" Module for Average Result class """

from sqlalchemy import Column, String, Integer, ForeignKey, Float
from models.engine.db_storage import BaseModel, Base

class AVRGSubject(BaseModel, Base):
    __tablename__ = 'average_subject'
    student_id = Column(String(120), ForeignKey('student.id'), nullable=False)
    grade_id = Column(String(120), ForeignKey('grades.id'), nullable=False)
    section_id = Column(String(120), ForeignKey('sections.id'), nullable=False)
    subject_id = Column(String(120), ForeignKey('subjects.id'), nullable=False)
    teachers_record_id = Column(String(120), ForeignKey('teachers_record.id', ondelete="SET NULL"), nullable=True, default=None)
    average = Column(Float, default=None)  # The actual average score of the student in this for all subject
    rank = Column(Integer, default=None)
    year = Column(String(10), nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes score"""
        super().__init__(*args, **kwargs)
