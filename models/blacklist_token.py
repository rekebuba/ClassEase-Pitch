#!/usr/bin/python3
""" Module for Grade class """

from sqlalchemy import Column, String
from models.engine.db_storage import BaseModel, Base

class BlacklistToken(BaseModel, Base):
    jti = Column(String(120), nullable=False, unique=True)
