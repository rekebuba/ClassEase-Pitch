"""trigger for class_section to check stream_id

Revision ID: 7c8fbb47e921
Revises: b3a97b08e1cb
Create Date: 2026-07-20 18:48:09.130059

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7c8fbb47e921"
down_revision: Union[str, Sequence[str], None] = "b3a97b08e1cb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 1. Create a function to validate the stream belongs to the grade
    op.execute("""
        CREATE OR REPLACE FUNCTION validate_stream_grade()
        RETURNS TRIGGER AS $$
        BEGIN
            IF NEW.stream_id IS NOT NULL THEN
                IF NOT EXISTS (
                    SELECT 1 FROM public.streams s
                    JOIN public.sections sec ON sec.grade_id = s.grade_id
                    WHERE s.id = NEW.stream_id AND sec.id = NEW.section_id
                ) THEN
                    RAISE EXCEPTION 'The selected stream does not belong to the grade associated with this section.';
                END IF;
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    # 2. Attach the trigger to the class_sections table
    op.execute("""
        CREATE TRIGGER trg_validate_class_section_stream
        BEFORE INSERT OR UPDATE ON public.class_sections
        FOR EACH ROW EXECUTE FUNCTION validate_stream_grade();
    """)


def downgrade():
    op.execute("DROP TRIGGER IF EXISTS trg_validate_class_section_stream ON public.class_sections;")
    op.execute("DROP FUNCTION IF EXISTS validate_stream_grade();")
