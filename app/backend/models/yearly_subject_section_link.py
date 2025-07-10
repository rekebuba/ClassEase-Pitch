#!/usr/bin/python3

from dataclasses import dataclass
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlmodel import ForeignKey
from models.base_model import Base


@dataclass
class YearlySubjectSectionLink(Base):
    __tablename__ = "yearly_subject_section_links"

    section_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("sections.id"),
        primary_key=True,
    )
    yearly_subject_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("yearly_subjects.id"),
        primary_key=True,
    )
