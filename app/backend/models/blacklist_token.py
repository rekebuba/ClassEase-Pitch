#!/usr/bin/python3
"""Module for Grade class"""

from sqlalchemy import String
from models.base.base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column


class BlacklistToken(BaseModel):
    __tablename__ = "blacklist_tokens"
    jti: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
