"""enable rls on tenant tables

Revision ID: 6c1b8c9f0a21
Revises: 39de98d12662
Create Date: 2026-04-30 20:45:00.000000

"""

import uuid
from typing import Sequence, Union

from alembic import op
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = "6c1b8c9f0a21"
down_revision: Union[str, Sequence[str], None] = "39de98d12662"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TENANT_TABLES: tuple[str, ...] = (
    "academic_terms",
    "admins",
    "employees",
    "events",
    "grades",
    "sections",
    "streams",
    "students",
    "subjects",
    "parents",
    "years",
    "audit_logs",
    "auth_sessions",
    "school_memberships",
    "roles",
    "transfer_requests",
)

SCHOOL_ID_TABLES: tuple[str, ...] = (
    "academic_terms",
    "admins",
    "employees",
    "events",
    "grades",
    "sections",
    "streams",
    "students",
    "subjects",
    "parents",
    "years",
    "audit_logs",
    "auth_sessions",
    "school_memberships",
    "roles",
)

TENANT_ID_EXPR = "NULLIF(current_setting('app.current_school_id', true), '')::uuid"
TRANSFER_EXPR = (
    f"source_school_id = {TENANT_ID_EXPR} OR target_school_id = {TENANT_ID_EXPR}"
)


LEGACY_NAME = "Legacy School"
LEGACY_SLUG = "legacy"
ID = str(uuid.uuid4())


def _policy_name(table_name: str) -> str:
    return f"rls_{table_name}_tenant_isolation"


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()

    legacy_school_id = bind.execute(
        text("SELECT id FROM schools WHERE slug = :slug"),
        {"slug": "legacy"},
    ).scalar_one_or_none()

    # If it doesn't exist (e.g., fresh DB), create it
    if legacy_school_id is None:
        bind.execute(
            text("""
            INSERT INTO schools (id, name, slug, status, settings)
            VALUES (
                :id,
                :name,
                :slug,
                'active',
                :settings
            )
            """),
            {
                "id": ID,
                "name": LEGACY_NAME,
                "slug": LEGACY_SLUG,
                "settings": '{"bootstrapMode": "legacy"}',
            },
        )
        # Fetch the ID of the record we just created
        legacy_school_id = bind.execute(
            text("SELECT id FROM schools WHERE slug = :slug"),
            {"slug": "legacy"},
        ).scalar_one()

    for table_name in SCHOOL_ID_TABLES:
        bind.execute(
            text(
                f"UPDATE {table_name} SET school_id = :school_id WHERE school_id IS NULL"  # noqa: E501
            ),
            {"school_id": legacy_school_id},
        )

    for table_name in TENANT_TABLES:
        policy_name = _policy_name(table_name)
        policy_expr = (
            TRANSFER_EXPR
            if table_name == "transfer_requests"
            else f"school_id = {TENANT_ID_EXPR}"
        )

        op.execute(f"ALTER TABLE {table_name} ENABLE ROW LEVEL SECURITY")
        op.execute(f"ALTER TABLE {table_name} FORCE ROW LEVEL SECURITY")
        op.execute(f"DROP POLICY IF EXISTS {policy_name} ON {table_name}")
        op.execute(
            f"CREATE POLICY {policy_name} "
            f"ON {table_name} FOR ALL "
            f"USING ({policy_expr}) "
            f"WITH CHECK ({policy_expr})"
        )


def downgrade() -> None:
    """Downgrade schema."""
    for table_name in reversed(TENANT_TABLES):
        policy_name = _policy_name(table_name)
        op.execute(f"DROP POLICY IF EXISTS {policy_name} ON {table_name}")
        op.execute(f"ALTER TABLE {table_name} NO FORCE ROW LEVEL SECURITY")
        op.execute(f"ALTER TABLE {table_name} DISABLE ROW LEVEL SECURITY")
