#!/usr/bin/python3

from sqlalchemy import Column, Integer, String, ForeignKey
from models.engine.db_storage import BaseModel, Base


class Subject(BaseModel, Base):
    __tablename__ = 'subjects'
    name = Column(String(50), nullable=False)
    code = Column(String(10), nullable=False)
    grade_id = Column(String(120), ForeignKey('grades.id'), nullable=False)
    teacher_id = Column(String(120), ForeignKey('teacher.id', ondelete="SET NULL"), nullable=True, default=None)
    school_year = Column(String(10), nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes score"""
        super().__init__(*args, **kwargs)
