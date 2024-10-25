#!/usr/bin/python3

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.engine.db_storage import BaseModel, Base


class TeachersRecord(BaseModel, Base):
    __tablename__ = 'teachers_record'
    teacher_id = Column(String(120), ForeignKey(
        'teacher.id'), nullable=False)
    subject_id = Column(String(120), ForeignKey(
        'subjects.id'), nullable=True, default=None)
    grade_id = Column(String(120), ForeignKey(
        'grades.id'), nullable=True, default=None)
    section_id = Column(String(120), ForeignKey(
        'sections.id'), nullable=True, default=None)

    mark_list = relationship(
        "MarkList", backref="teachers_record", cascade="save-update", passive_deletes=True)

    def __init__(self, *args, **kwargs):
        """initializes score"""
        super().__init__(*args, **kwargs)
