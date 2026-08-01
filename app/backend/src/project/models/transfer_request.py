import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, Optional

from sqlalchemy import (
    UUID,
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    ForeignKeyConstraint,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.utils.enum import TransferRequestStatusEnum

if TYPE_CHECKING:
    from project.models.school import School
    from project.models.school_membership import SchoolMembership


class TransferRequest(BaseModel):
    __tablename__ = "transfer_requests"

    source_school_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("schools.id", ondelete="CASCADE"),
        nullable=False,
    )
    target_school_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("schools.id", ondelete="CASCADE"),
        nullable=False,
    )
    subject_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    record_scope: Mapped[str] = mapped_column(String(120), nullable=False)
    requested_by_membership_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(),
        nullable=True,
        default=None,
    )
    reviewed_by_membership_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(),
        nullable=True,
        default=None,
    )
    status: Mapped[TransferRequestStatusEnum] = mapped_column(
        Enum(
            TransferRequestStatusEnum,
            name="transfer_request_status_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
        default=TransferRequestStatusEnum.PENDING,
    )
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default=None)
    payload: Mapped[Dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default_factory=dict,
    )
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )

    __table_args__ = (
        CheckConstraint(
            "source_school_id <> target_school_id",
            name="ck_source_target_different",
        ),
        ForeignKeyConstraint(
            ["requested_by_membership_id", "source_school_id"],
            ["school_memberships.id", "school_memberships.school_id"],
            name="fk_transfer_request_requested_by",
        ),
        ForeignKeyConstraint(
            ["reviewed_by_membership_id", "target_school_id"],
            ["school_memberships.id", "school_memberships.school_id"],
            name="fk_transfer_request_reviewed_by",
        ),
    )

    source_school: Mapped["School"] = relationship(
        "School",
        foreign_keys=[source_school_id],
        back_populates="initiated_transfers",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    target_school: Mapped["School"] = relationship(
        "School",
        foreign_keys=[target_school_id],
        back_populates="received_transfers",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    requested_by_membership: Mapped[Optional["SchoolMembership"]] = relationship(
        "SchoolMembership",
        foreign_keys=[requested_by_membership_id],
        back_populates="initiated_transfers",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    reviewed_by_membership: Mapped[Optional["SchoolMembership"]] = relationship(
        "SchoolMembership",
        foreign_keys=[reviewed_by_membership_id],
        back_populates="reviewed_transfers",
        init=False,
        repr=False,
        passive_deletes=True,
    )
