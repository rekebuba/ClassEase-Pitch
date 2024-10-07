
#!/usr/bin/python3

from sqlalchemy import Column, String, Integer, ForeignKey, Float
from models.engine.db_storage import BaseModel, Base

class Assessment(BaseModel, Base):
    __tablename__ = 'assessments'
    student_id = Column(String(120), ForeignKey('students.id'), nullable=False)
    subject_id = Column(String(120), ForeignKey('subjects.id'), nullable=False)
    average = Column(Float, default=0)  # The actual score of the student in this assessment
    semester = Column(Integer, nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes score"""
        super().__init__(*args, **kwargs)
