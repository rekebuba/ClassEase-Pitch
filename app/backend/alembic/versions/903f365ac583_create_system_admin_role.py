"""{create_settings.POSTGRES_SYSTEM_ROLE}_role

Revision ID: 903f365ac583
Revises: 5668cfae5856
Create Date: 2026-06-28 21:34:50.276677

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

from project.core.config import settings

# revision identifiers, used by Alembic.
revision: str = "903f365ac583"
down_revision: Union[str, Sequence[str], None] = "5668cfae5856"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # It is best practice to use a connection-based execution for DCL
    conn = op.get_bind()

    # We execute these as raw SQL because Alembic's 'op'
    # doesn't have dedicated helpers for ROLE management.
    conn.execute(
        sa.text(
            f"CREATE ROLE {settings.POSTGRES_SYSTEM_ROLE} \
            WITH LOGIN PASSWORD '{settings.POSTGRES_SYSTEM_PASS.get_secret_value()}';"
        )
    )
    conn.execute(sa.text(f"ALTER ROLE {settings.POSTGRES_SYSTEM_ROLE} BYPASSRLS;"))

    # Grant permissions
    conn.execute(sa.text(f"GRANT USAGE ON SCHEMA public TO {settings.POSTGRES_SYSTEM_ROLE};"))
    conn.execute(
        sa.text(
            f"GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO {settings.POSTGRES_SYSTEM_ROLE};"
        )
    )
    conn.execute(sa.text(f"GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO {settings.POSTGRES_SYSTEM_ROLE};"))


def downgrade():
    # Clean up by dropping the role
    conn = op.get_bind()

    # 1. Revoke privileges from the role
    conn.execute(sa.text("REVOKE ALL ON ALL TABLES IN SCHEMA public FROM system_admin;"))
    conn.execute(sa.text("REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM system_admin;"))
    conn.execute(sa.text("REVOKE ALL ON SCHEMA public FROM system_admin;"))

    # 2. Drop the role
    conn.execute(sa.text("DROP ROLE IF EXISTS system_admin;"))
