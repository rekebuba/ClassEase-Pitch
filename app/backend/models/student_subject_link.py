#!/usr/bin/python3

from sqlalchemy import Float, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlmodel import ForeignKey
from models.base.base_model import BaseModel
from models.base.column_type import UUIDType
import uuid


class StudentTermSubject(BaseModel):
    __tablename__ = "student_term_subjects"

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("students.id"),
        primary_key=True,
    )
    subject_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("subjects.id"),
        primary_key=True,
    )
    academic_term_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("academic_terms.id"),
        primary_key=True,
    )

    average: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    rank: Mapped[int] = mapped_column(Integer, nullable=True, default=None)
