#!/usr/bin/python3
from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, Float
from models.engine.db_storage import BaseModel, Base
from ethiopian_date import EthiopianDateConverter
import random
from datetime import datetime


class Student(BaseModel, Base):
    __tablename__ = 'students'
    id = Column(String(120), primary_key=True, unique=True)
    first_name = Column(String(50), nullable=False)
    father_name = Column(String(50), nullable=False)
    g_father_name = Column(String(50))
    age = Column(Integer, nullable=False)
    password = Column(String(120))
    father_phone = Column(String(15))
    mother_phone = Column(String(15))

    grade_id = Column(String(120), ForeignKey('grades.id'), nullable=False)
    section_id = Column(String(120), ForeignKey('sections.id'))

    semester_1_average = Column(Float)
    semester_2_average = Column(Float)
    semester_1_rank = Column(Float)
    semester_2_rank = Column(Float)

    __table_args__ = (
        CheckConstraint(
            'father_phone IS NOT NULL OR mother_phone IS NOT NULL'),
    )

    def __init__(self, *args, **kwargs):
        """initializes score"""
        super().__init__(*args, **kwargs)
        self.id = self.generate_student_id(kwargs['grade'])


    def generate_student_id(self, grade):
        """Function to generate a custom student ID based on the grade"""
        id = ''
        section = ''
        if grade < 8:
            section = 'ELM'
        elif grade > 8 and grade < 11:
            section = 'HIG'
        else:
            section = 'PRE'
        unique = True
        while unique:
            num = random.randint(1000, 9999)
            starting_year = EthiopianDateConverter.date_to_ethiopian(datetime.now()).year % 100
            id = f'{section}/{num}/{starting_year}/{grade}'
            if not self.id_exists(id):
                unique = False
        return id

    def id_exists(self, id):
        """Function to check if the student ID already exists"""
        from models import storage
        if storage._DBStorage__session.query(Student).filter_by(id=id).first():
            return True
        return False
