#!/usr/bin/python3

from dataclasses import dataclass
from sqlalchemy.orm import Mapped, mapped_column
from sqlmodel import ForeignKey
from models.base.base_model import Base
from models.base.column_type import UUIDType
import uuid


@dataclass
class TeacherYearLink(Base):
    __tablename__ = "teacher_year_links"

    teacher_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("teachers.id"),
        primary_key=True,
    )
    year_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("years.id"),
        primary_key=True,
    )
