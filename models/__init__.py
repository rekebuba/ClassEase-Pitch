#!/usr/bin/python3

from models.engine.db_storage import DBStorage
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

storage = DBStorage()
storage.reload()


# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
# from models.engine.db_storage import Base

# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(100), nullable=False)
#     email = Column(String(100), nullable=False, unique=True)
#     password = Column(String(100), nullable=False)

#     # Define relationships
#     grades = relationship("Grade", backref="user", cascade="all, delete-orphan")

# class Score(Base):
#     __tablename__ = 'classes'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     class_name = Column(String(100), nullable=False)
#     teacher = Column(String(100), nullable=False)

#     # Define relationships
#     grades = relationship("Grade", backref="class", cascade="all, delete-orphan")

# class Paragraph(Base):
#     __tablename__ = 'grades'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
#     class_id = Column(Integer, ForeignKey('classes.id'), nullable=False)
#     grade = Column(String(2), nullable=False)
