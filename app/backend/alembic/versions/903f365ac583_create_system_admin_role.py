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


# Assuming your settings module is imported in your migration script:
# from app.core.config import settings


def upgrade():
    conn = op.get_bind()

    system_role = settings.POSTGRES_SYSTEM_ROLE
    system_pass = settings.POSTGRES_SYSTEM_PASS.get_secret_value()
    primary_user = settings.POSTGRES_USER  # Ensure primary user variable is available

    # 1. Create role safely if it doesn't exist
    conn.execute(
        sa.text(
            f"""
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = '{system_role}') THEN
                    CREATE ROLE {system_role} WITH LOGIN PASSWORD '{system_pass}';
                END IF;
            END
            $$;
            """
        )
    )

    # 2. Grant role options & database access
    conn.execute(sa.text(f"ALTER ROLE {system_role} BYPASSRLS;"))
    conn.execute(sa.text(f"GRANT CONNECT ON DATABASE {settings.POSTGRES_DB} TO {system_role};"))
    conn.execute(sa.text(f"GRANT USAGE, CREATE ON SCHEMA public TO {system_role};"))

    # 3. Existing objects permissions
    conn.execute(sa.text(f"GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO {system_role};"))
    conn.execute(sa.text(f"GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO {system_role};"))
    conn.execute(sa.text(f"GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO {system_role};"))

    # 4. Future objects created by primary user -> granted to system role
    conn.execute(
        sa.text(
            f"ALTER DEFAULT PRIVILEGES FOR USER {primary_user} IN SCHEMA public "
            f"GRANT ALL PRIVILEGES ON TABLES TO {system_role};"
        )
    )
    conn.execute(
        sa.text(
            f"ALTER DEFAULT PRIVILEGES FOR USER {primary_user} IN SCHEMA public "
            f"GRANT ALL PRIVILEGES ON SEQUENCES TO {system_role};"
        )
    )
    conn.execute(
        sa.text(
            f"ALTER DEFAULT PRIVILEGES FOR USER {primary_user} IN SCHEMA public "
            f"GRANT ALL PRIVILEGES ON FUNCTIONS TO {system_role};"
        )
    )

    # 5. Future objects created by system role -> granted to primary user
    conn.execute(
        sa.text(
            f"ALTER DEFAULT PRIVILEGES FOR USER {system_role} IN SCHEMA public "
            f"GRANT ALL PRIVILEGES ON TABLES TO {primary_user};"
        )
    )
    conn.execute(
        sa.text(
            f"ALTER DEFAULT PRIVILEGES FOR USER {system_role} IN SCHEMA public "
            f"GRANT ALL PRIVILEGES ON SEQUENCES TO {primary_user};"
        )
    )
    conn.execute(
        sa.text(
            f"ALTER DEFAULT PRIVILEGES FOR USER {system_role} IN SCHEMA public "
            f"GRANT ALL PRIVILEGES ON FUNCTIONS TO {primary_user};"
        )
    )


def downgrade():
    conn = op.get_bind()

    system_role = settings.POSTGRES_SYSTEM_ROLE
    primary_user = settings.POSTGRES_USER

    # 1. Revoke default privileges
    conn.execute(
        sa.text(
            f"ALTER DEFAULT PRIVILEGES FOR USER {primary_user} IN SCHEMA public "
            f"REVOKE ALL ON TABLES FROM {system_role};"
        )
    )
    conn.execute(
        sa.text(
            f"ALTER DEFAULT PRIVILEGES FOR USER {primary_user} IN SCHEMA public "
            f"REVOKE ALL ON SEQUENCES FROM {system_role};"
        )
    )
    conn.execute(
        sa.text(
            f"ALTER DEFAULT PRIVILEGES FOR USER {primary_user} IN SCHEMA public "
            f"REVOKE ALL ON FUNCTIONS FROM {system_role};"
        )
    )
    conn.execute(
        sa.text(
            f"ALTER DEFAULT PRIVILEGES FOR USER {system_role} IN SCHEMA public "
            f"REVOKE ALL ON TABLES FROM {primary_user};"
        )
    )
    conn.execute(
        sa.text(
            f"ALTER DEFAULT PRIVILEGES FOR USER {system_role} IN SCHEMA public "
            f"REVOKE ALL ON SEQUENCES FROM {primary_user};"
        )
    )
    conn.execute(
        sa.text(
            f"ALTER DEFAULT PRIVILEGES FOR USER {system_role} IN SCHEMA public "
            f"REVOKE ALL ON FUNCTIONS FROM {primary_user};"
        )
    )

    # 2. Revoke existing object privileges
    conn.execute(sa.text(f"REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM {system_role};"))
    conn.execute(sa.text(f"REVOKE ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public FROM {system_role};"))
    conn.execute(sa.text(f"REVOKE ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public FROM {system_role};"))
    conn.execute(sa.text(f"REVOKE ALL ON SCHEMA public FROM {system_role};"))
    conn.execute(sa.text(f"REVOKE CONNECT ON DATABASE {settings.POSTGRES_DB} FROM {system_role};"))

    # 3. Drop role
    conn.execute(sa.text(f"DROP ROLE IF EXISTS {system_role};"))
