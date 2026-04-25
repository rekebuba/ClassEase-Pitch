import uuid

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, MappedAsDataclass, declarative_mixin, mapped_column


@declarative_mixin
class SchoolScopedMixin(MappedAsDataclass):
    """Mixin for tenant-owned rows."""

    school_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(),
        ForeignKey("schools.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
        init=False,
    )
