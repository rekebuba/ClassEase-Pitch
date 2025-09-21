import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base.base_model import BaseModel
from models.base.column_type import UUIDType

if TYPE_CHECKING:
    from models.section import Section
    from models.teacher_record import TeacherRecord


class TeacherRecordLink(BaseModel):
    __tablename__ = "teacher_record_links"

    teacher_record_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("teacher_records.id", ondelete="CASCADE"),
        nullable=False,
    )
    section_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("sections.id", ondelete="CASCADE"),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "teacher_record_id",
            "section_id",
            name="uq_teacher_record",
        ),
    )
