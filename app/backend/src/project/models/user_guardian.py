import uuid

from sqlalchemy import UUID, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from project.models.base.base_model import BaseModel


class UserGuardian(BaseModel):
    """
    Represents a link between a parent and a student in the database.
    This link is global (User to User).
    """

    __tablename__ = "user_guardians"

    guardian_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    dependent_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    relation: Mapped[str] = mapped_column(String(50), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "guardian_user_id",
            "dependent_user_id",
            name="uq_user_guardians",
        ),
    )
