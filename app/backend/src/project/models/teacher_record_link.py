import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from project.models.base.base_model import BaseModel

if TYPE_CHECKING:
    pass


class TeacherRecordLink(BaseModel):
    __tablename__ = "teacher_record_links"

    teacher_record_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("teacher_records.id", ondelete="CASCADE"),
        nullable=False,
    )
    section_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("sections.id", ondelete="CASCADE"),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "teacher_record_id",
            "section_id",
            name="uq_teacher_record_links",
        ),
    )
