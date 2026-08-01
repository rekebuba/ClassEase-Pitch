"""constraint on employee table

Revision ID: a6a18bbf41a2
Revises: 7b048703b9c8
Create Date: 2026-05-12 11:37:00.950185

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a6a18bbf41a2"
down_revision: Union[str, Sequence[str], None] = "7b048703b9c8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_foreign_key(
        "fk_employees_membership_school",
        "employees",
        "school_memberships",
        ["user_id", "school_id"],
        ["user_id", "school_id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "fk_employees_membership_school",
        "employees",
        type_="foreignkey",
    )
