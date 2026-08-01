"""student yearly grading

Revision ID: 76a074410a21
Revises: e95d6aaac4d4
Create Date: 2026-06-21 12:39:35.724453

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "76a074410a21"
down_revision: Union[str, Sequence[str], None] = "e95d6aaac4d4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands reordered for dependency correctness - see migration notes ###

    # ------------------------------------------------------------------
    # STEP 1: Unique constraints on existing parent tables that will be
    # targeted by composite FKs later in this migration. These must all
    # exist BEFORE any composite FK referencing (id, school_id) on these
    # tables is created.
    # ------------------------------------------------------------------
    op.create_unique_constraint("uq_academic_term_id_school_id", "academic_terms", ["id", "school_id"])

    # student_term_records.school_id must exist before we can build the
    # (id, school_id) unique constraint on it, and that unique constraint
    # must exist before subject_term_results' composite FK back to
    # student_term_records is created further down.
    op.add_column("student_term_records", sa.Column("school_id", sa.UUID(), nullable=True))
    op.create_index(
        op.f("ix_student_term_records_school_id"),
        "student_term_records",
        ["school_id"],
        unique=False,
    )
    op.create_unique_constraint(
        "uq_student_term_record_id_school_id",
        "student_term_records",
        ["id", "school_id"],
    )

    # student_year_records.school_id already exists from a prior migration.
    # We only need the (id, school_id) unique constraint here, ahead of
    # the composite FK on student_term_records that references it below.
    op.create_unique_constraint(
        "uq_student_year_record_id_school_id",
        "student_year_records",
        ["id", "school_id"],
    )

    # ------------------------------------------------------------------
    # STEP 2: Create new child tables. All composite-FK targets
    # (academic_terms, student_term_records, subject_offerings,
    # assessment_components, subject_term_results, teacher_profiles,
    # teaching_assignments) now have their required unique constraints
    # in place from STEP 1 (or pre-existing migrations / inline table-level
    # unique constraints created within this same create_table call).
    # ------------------------------------------------------------------
    op.create_table(
        "assessment_components",
        sa.Column("term_id", sa.UUID(), nullable=False),
        sa.Column("subject_offering_id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("weight", sa.Float(), nullable=False),
        sa.Column("max_score", sa.Float(), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.Column("school_id", sa.UUID(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["school_id"],
            ["schools.id"],
            name=op.f("fk_assessment_components_school_id_schools"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["subject_offering_id", "school_id"],
            ["subject_offerings.id", "subject_offerings.school_id"],
            name="fk_assessment_component_subject_offering_school",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["term_id", "school_id"],
            ["academic_terms.id", "academic_terms.school_id"],
            name="fk_assessment_component_term_school",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_assessment_components")),
        sa.UniqueConstraint("id", "school_id", name="uq_assessment_component_id_school_id"),
        sa.UniqueConstraint(
            "school_id",
            "term_id",
            "subject_offering_id",
            "name",
            name="uq_assessment_component_scheme_name",
        ),
    )
    op.create_index(
        op.f("ix_assessment_components_school_id"),
        "assessment_components",
        ["school_id"],
        unique=False,
    )

    op.create_table(
        "subject_term_results",
        sa.Column("student_term_record_id", sa.UUID(), nullable=False),
        sa.Column("subject_offering_id", sa.UUID(), nullable=False),
        sa.Column("total", sa.Float(), nullable=True),
        sa.Column("grade", sa.String(length=10), nullable=True),
        sa.Column("rank", sa.Integer(), nullable=True),
        sa.Column("pass_status", sa.String(length=20), nullable=True),
        sa.Column("teacher_remarks", sa.String(length=255), nullable=True),
        sa.Column("school_id", sa.UUID(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["school_id"],
            ["schools.id"],
            name=op.f("fk_subject_term_results_school_id_schools"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["student_term_record_id", "school_id"],
            ["student_term_records.id", "student_term_records.school_id"],
            name="fk_subject_term_result_student_term_record_school",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["subject_offering_id", "school_id"],
            ["subject_offerings.id", "subject_offerings.school_id"],
            name="fk_subject_term_result_subject_offering_school",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_subject_term_results")),
        sa.UniqueConstraint("id", "school_id", name="uq_subject_term_result_id_school_id"),
        sa.UniqueConstraint(
            "school_id",
            "student_term_record_id",
            "subject_offering_id",
            name="uq_subject_term_result_term_subject",
        ),
    )
    op.create_index(
        op.f("ix_subject_term_results_school_id"),
        "subject_term_results",
        ["school_id"],
        unique=False,
    )

    op.create_table(
        "assessment_scores",
        sa.Column("subject_term_result_id", sa.UUID(), nullable=False),
        sa.Column("assessment_component_id", sa.UUID(), nullable=False),
        sa.Column("remarks", sa.String(length=255), nullable=True),
        sa.Column("raw_score", sa.Float(), nullable=False),
        sa.Column("teaching_assignment_id", sa.UUID(), nullable=True),
        sa.Column("entered_by_teacher_profile_id", sa.UUID(), nullable=True),
        sa.Column("weighted_score", sa.Float(), nullable=True),
        sa.Column("entered_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("school_id", sa.UUID(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["assessment_component_id", "school_id"],
            ["assessment_components.id", "assessment_components.school_id"],
            name="fk_assessment_score_component_school",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["entered_by_teacher_profile_id", "school_id"],
            ["teacher_profiles.id", "teacher_profiles.school_id"],
            name="fk_assessment_score_entered_by_teacher_school",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["school_id"],
            ["schools.id"],
            name=op.f("fk_assessment_scores_school_id_schools"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["subject_term_result_id", "school_id"],
            ["subject_term_results.id", "subject_term_results.school_id"],
            name="fk_assessment_score_subject_term_result_school",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["teaching_assignment_id", "school_id"],
            ["teaching_assignments.id", "teaching_assignments.school_id"],
            name="fk_assessment_score_teaching_assignment_school",
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_assessment_scores")),
        sa.UniqueConstraint("id", "school_id", name="uq_assessment_score_id_school_id"),
        sa.UniqueConstraint(
            "school_id",
            "subject_term_result_id",
            "assessment_component_id",
            name="uq_assessment_score_result_component",
        ),
    )
    op.create_index(
        op.f("ix_assessment_scores_school_id"),
        "assessment_scores",
        ["school_id"],
        unique=False,
    )

    # ------------------------------------------------------------------
    # STEP 3: Drop the now-superseded "assessments" table. No remaining
    # table holds a live FK pointing into "assessments", so this is safe
    # now that its replacement tables exist.
    # ------------------------------------------------------------------
    op.drop_table("assessments")

    # ------------------------------------------------------------------
    # STEP 4: Add remaining new columns to student_term_records.
    # (school_id was already added in STEP 1, ahead of subject_term_results.)
    # ------------------------------------------------------------------
    op.add_column(
        "student_term_records",
        sa.Column("student_enrollment_id", sa.UUID(), nullable=False),
    )
    op.add_column(
        "student_term_records",
        sa.Column("student_year_record_id", sa.UUID(), nullable=True),
    )
    op.add_column(
        "student_term_records",
        sa.Column("pass_status", sa.String(length=20), nullable=True),
    )
    op.add_column(
        "student_term_records",
        sa.Column("teacher_remarks", sa.String(length=255), nullable=True),
    )

    op.create_unique_constraint(
        "uq_student_term_record_enrollment_term",
        "student_term_records",
        ["school_id", "student_enrollment_id", "academic_term_id"],
    )

    # ------------------------------------------------------------------
    # STEP 5: Swap student_term_records' single-column legacy FKs for the
    # new school-scoped composite FKs. Old FKs are dropped before the
    # columns they reference get dropped later in STEP 6.
    # ------------------------------------------------------------------
    op.drop_constraint(
        op.f("fk_student_term_records_student_id_students"),
        "student_term_records",
        type_="foreignkey",
    )
    op.drop_constraint(
        op.f("fk_student_term_records_section_id_sections"),
        "student_term_records",
        type_="foreignkey",
    )
    op.drop_constraint(
        op.f("fk_student_term_records_grade_id_grades"),
        "student_term_records",
        type_="foreignkey",
    )
    op.drop_constraint(
        op.f("fk_student_term_records_academic_term_id_academic_terms"),
        "student_term_records",
        type_="foreignkey",
    )
    op.drop_constraint(
        op.f("fk_student_term_records_stream_id_streams"),
        "student_term_records",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "fk_student_term_record_enrollment_school",
        "student_term_records",
        "student_enrollments",
        ["student_enrollment_id", "school_id"],
        ["id", "school_id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        op.f("fk_student_term_records_school_id_schools"),
        "student_term_records",
        "schools",
        ["school_id"],
        ["id"],
        ondelete="CASCADE",
    )
    # Requires uq_student_year_record_id_school_id, created in STEP 1.
    op.create_foreign_key(
        "fk_student_term_record_year_record_school",
        "student_term_records",
        "student_year_records",
        ["student_year_record_id", "school_id"],
        ["id", "school_id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_student_term_record_academic_term_school",
        "student_term_records",
        "academic_terms",
        ["academic_term_id", "school_id"],
        ["id", "school_id"],
        ondelete="CASCADE",
    )

    # ------------------------------------------------------------------
    # STEP 6: Drop the now-unreferenced legacy columns on
    # student_term_records (their FKs were already dropped in STEP 5).
    # ------------------------------------------------------------------
    op.drop_column("student_term_records", "student_id")
    op.drop_column("student_term_records", "grade_id")
    op.drop_column("student_term_records", "stream_id")
    op.drop_column("student_term_records", "section_id")

    # ------------------------------------------------------------------
    # STEP 7: student_year_records column/FK migration.
    # (uq_student_year_record_id_school_id was already created in STEP 1.)
    # ------------------------------------------------------------------
    op.add_column(
        "student_year_records",
        sa.Column("student_enrollment_id", sa.UUID(), nullable=False),
    )
    op.add_column(
        "student_year_records",
        sa.Column("promotion_status", sa.String(length=30), nullable=True),
    )

    op.create_unique_constraint(
        "uq_student_year_record_enrollment",
        "student_year_records",
        ["school_id", "student_enrollment_id"],
    )

    op.drop_constraint(
        op.f("fk_student_year_records_student_school"),
        "student_year_records",
        type_="foreignkey",
    )
    op.drop_constraint(
        op.f("fk_student_year_records_grade_school"),
        "student_year_records",
        type_="foreignkey",
    )
    op.drop_constraint(
        op.f("fk_student_year_records_stream_school"),
        "student_year_records",
        type_="foreignkey",
    )
    op.drop_constraint(
        op.f("fk_student_year_records_year_school"),
        "student_year_records",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "fk_student_year_record_enrollment_school",
        "student_year_records",
        "student_enrollments",
        ["student_enrollment_id", "school_id"],
        ["id", "school_id"],
        ondelete="CASCADE",
    )

    op.drop_column("student_year_records", "year_id")
    op.drop_column("student_year_records", "student_id")
    op.drop_column("student_year_records", "grade_id")
    op.drop_column("student_year_records", "stream_id")

    # ------------------------------------------------------------------
    # STEP 8: subject_yearly_averages column/FK migration.
    # ------------------------------------------------------------------
    op.add_column(
        "subject_yearly_averages",
        sa.Column("grade", sa.String(length=10), nullable=True),
    )
    op.add_column("subject_yearly_averages", sa.Column("school_id", sa.UUID(), nullable=True))
    op.alter_column(
        "subject_yearly_averages",
        "student_year_record_id",
        existing_type=sa.UUID(),
        nullable=False,
    )
    op.create_index(
        op.f("ix_subject_yearly_averages_school_id"),
        "subject_yearly_averages",
        ["school_id"],
        unique=False,
    )
    op.create_unique_constraint(
        "uq_subject_yearly_average_id_school_id",
        "subject_yearly_averages",
        ["id", "school_id"],
    )
    op.create_unique_constraint(
        "uq_subject_yearly_average_record_subject",
        "subject_yearly_averages",
        ["school_id", "student_year_record_id", "subject_offering_id"],
    )

    op.drop_constraint(
        op.f("fk_subject_yearly_averages_student_year_record_id_stude_1781"),
        "subject_yearly_averages",
        type_="foreignkey",
    )
    op.drop_constraint(
        op.f("fk_subject_yearly_averages_student_id_students"),
        "subject_yearly_averages",
        type_="foreignkey",
    )
    op.drop_constraint(
        op.f("fk_subject_yearly_averages_subject_offering_id_subject__ee48"),
        "subject_yearly_averages",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "fk_subject_yearly_average_year_record_school",
        "subject_yearly_averages",
        "student_year_records",
        ["student_year_record_id", "school_id"],
        ["id", "school_id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_subject_yearly_average_subject_offering_school",
        "subject_yearly_averages",
        "subject_offerings",
        ["subject_offering_id", "school_id"],
        ["id", "school_id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        op.f("fk_subject_yearly_averages_school_id_schools"),
        "subject_yearly_averages",
        "schools",
        ["school_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.drop_column("subject_yearly_averages", "student_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands reordered for dependency correctness - see migration notes ###

    # ------------------------------------------------------------------
    # STEP 1: Reverse subject_yearly_averages changes.
    # ------------------------------------------------------------------
    op.add_column(
        "subject_yearly_averages",
        sa.Column("student_id", sa.UUID(), autoincrement=False, nullable=False),
    )

    op.drop_constraint(
        op.f("fk_subject_yearly_averages_school_id_schools"),
        "subject_yearly_averages",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_subject_yearly_average_subject_offering_school",
        "subject_yearly_averages",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_subject_yearly_average_year_record_school",
        "subject_yearly_averages",
        type_="foreignkey",
    )

    op.create_foreign_key(
        op.f("fk_subject_yearly_averages_subject_offering_id_subject__ee48"),
        "subject_yearly_averages",
        "subject_offerings",
        ["subject_offering_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        op.f("fk_subject_yearly_averages_student_id_students"),
        "subject_yearly_averages",
        "students",
        ["student_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        op.f("fk_subject_yearly_averages_student_year_record_id_stude_1781"),
        "subject_yearly_averages",
        "student_year_records",
        ["student_year_record_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.drop_constraint(
        "uq_subject_yearly_average_record_subject",
        "subject_yearly_averages",
        type_="unique",
    )
    op.drop_constraint(
        "uq_subject_yearly_average_id_school_id",
        "subject_yearly_averages",
        type_="unique",
    )
    op.drop_index(
        op.f("ix_subject_yearly_averages_school_id"),
        table_name="subject_yearly_averages",
    )
    op.alter_column(
        "subject_yearly_averages",
        "student_year_record_id",
        existing_type=sa.UUID(),
        nullable=True,
    )
    op.drop_column("subject_yearly_averages", "school_id")
    op.drop_column("subject_yearly_averages", "grade")

    # ------------------------------------------------------------------
    # STEP 2: Reverse student_year_records changes EXCEPT for dropping
    # uq_student_year_record_id_school_id. That drop is deferred to
    # STEP 4 because student_term_records' composite FK
    # fk_student_term_record_year_record_school still depends on it
    # (it isn't dropped until STEP 3) — dropping the unique constraint
    # here would fail with "cannot drop constraint ... because other
    # objects depend on it".
    # ------------------------------------------------------------------
    op.add_column(
        "student_year_records",
        sa.Column("stream_id", sa.UUID(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "student_year_records",
        sa.Column("grade_id", sa.UUID(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "student_year_records",
        sa.Column("student_id", sa.UUID(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "student_year_records",
        sa.Column("year_id", sa.UUID(), autoincrement=False, nullable=False),
    )

    op.drop_constraint(
        "fk_student_year_record_enrollment_school",
        "student_year_records",
        type_="foreignkey",
    )
    op.create_foreign_key(
        op.f("fk_student_year_records_year_school"),
        "student_year_records",
        "years",
        ["year_id", "school_id"],
        ["id", "school_id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        op.f("fk_student_year_records_stream_school"),
        "student_year_records",
        "streams",
        ["stream_id", "school_id"],
        ["id", "school_id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        op.f("fk_student_year_records_grade_school"),
        "student_year_records",
        "grades",
        ["grade_id", "school_id"],
        ["id", "school_id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        op.f("fk_student_year_records_student_school"),
        "student_year_records",
        "students",
        ["student_id", "school_id"],
        ["id", "school_id"],
        ondelete="CASCADE",
    )

    op.drop_constraint("uq_student_year_record_enrollment", "student_year_records", type_="unique")

    op.drop_column("student_year_records", "promotion_status")
    op.drop_column("student_year_records", "student_enrollment_id")

    # ------------------------------------------------------------------
    # STEP 3: Reverse student_term_records changes. The composite FK
    # fk_student_term_record_year_record_school (which depends on
    # uq_student_year_record_id_school_id on student_year_records) is
    # dropped here, BEFORE that unique constraint is removed in STEP 4.
    # ------------------------------------------------------------------
    op.add_column(
        "student_term_records",
        sa.Column("section_id", sa.UUID(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "student_term_records",
        sa.Column("stream_id", sa.UUID(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "student_term_records",
        sa.Column("grade_id", sa.UUID(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "student_term_records",
        sa.Column("student_id", sa.UUID(), autoincrement=False, nullable=False),
    )

    op.drop_constraint(
        "fk_student_term_record_academic_term_school",
        "student_term_records",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_student_term_record_year_record_school",
        "student_term_records",
        type_="foreignkey",
    )
    op.drop_constraint(
        op.f("fk_student_term_records_school_id_schools"),
        "student_term_records",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_student_term_record_enrollment_school",
        "student_term_records",
        type_="foreignkey",
    )

    op.create_foreign_key(
        op.f("fk_student_term_records_stream_id_streams"),
        "student_term_records",
        "streams",
        ["stream_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        op.f("fk_student_term_records_academic_term_id_academic_terms"),
        "student_term_records",
        "academic_terms",
        ["academic_term_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        op.f("fk_student_term_records_grade_id_grades"),
        "student_term_records",
        "grades",
        ["grade_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        op.f("fk_student_term_records_section_id_sections"),
        "student_term_records",
        "sections",
        ["section_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        op.f("fk_student_term_records_student_id_students"),
        "student_term_records",
        "students",
        ["student_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.drop_constraint("uq_student_term_record_enrollment_term", "student_term_records", type_="unique")

    op.drop_index(op.f("ix_student_term_records_school_id"), table_name="student_term_records")
    op.drop_column("student_term_records", "teacher_remarks")
    op.drop_column("student_term_records", "pass_status")
    op.drop_column("student_term_records", "student_year_record_id")
    op.drop_column("student_term_records", "student_enrollment_id")

    # ------------------------------------------------------------------
    # STEP 4: Now that fk_student_term_record_year_record_school has been
    # dropped (STEP 3), it is safe to drop
    # uq_student_year_record_id_school_id on student_year_records.
    # uq_student_term_record_id_school_id on student_term_records is
    # likewise still referenced by fk_subject_term_result_student_term_record_school
    # on subject_term_results, so its drop is deferred to STEP 6, after
    # subject_term_results is dropped. Same logic applies to
    # uq_academic_term_id_school_id, referenced by
    # fk_assessment_component_term_school on assessment_components, so it
    # too is deferred to STEP 6.
    # ------------------------------------------------------------------
    op.drop_constraint("uq_student_year_record_id_school_id", "student_year_records", type_="unique")

    # NOTE: student_term_records.school_id is intentionally NOT dropped
    # here. uq_student_term_record_id_school_id (a unique constraint
    # built on id+school_id) still covers this column at this point, and
    # it is not dropped until STEP 6 (after subject_term_results, whose
    # FK depends on it, has been dropped). Dropping the column now would
    # fail with "constraint ... depends on column school_id" while that
    # unique constraint still exists. school_id is dropped at the end of
    # STEP 6, immediately after that unique constraint is removed.

    # ------------------------------------------------------------------
    # STEP 5: Recreate the legacy "assessments" table. It only needs
    # single-column FKs to students.id, student_term_records.id, and
    # subject_offerings.id (all PKs), so it has no composite-unique-
    # constraint prerequisites and can be created any time after
    # student_term_records exists.
    # ------------------------------------------------------------------
    op.create_table(
        "assessments",
        sa.Column("student_id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column("student_term_record_id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column(
            "total",
            sa.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("rank", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("subject_offering_id", sa.UUID(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["student_id"],
            ["students.id"],
            name=op.f("fk_assessments_student_id_students"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["student_term_record_id"],
            ["student_term_records.id"],
            name=op.f("fk_assessments_student_term_record_id_student_term_records"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["subject_offering_id"],
            ["subject_offerings.id"],
            name=op.f("fk_assessments_subject_offering_id_subject_offerings"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_assessments")),
    )

    # ------------------------------------------------------------------
    # STEP 6: Drop the new child tables (children before parents from an
    # FK standpoint: assessment_scores references both subject_term_results
    # and assessment_components, so it must be dropped first). Dropping
    # each table automatically drops the composite FKs declared on it
    # (fk_subject_term_result_student_term_record_school and
    # fk_assessment_component_term_school among them), which finally
    # clears the way to drop the two remaining unique constraints that
    # were deferred from STEP 4.
    # ------------------------------------------------------------------
    op.drop_index(op.f("ix_assessment_scores_school_id"), table_name="assessment_scores")
    op.drop_table("assessment_scores")

    op.drop_index(op.f("ix_subject_term_results_school_id"), table_name="subject_term_results")
    op.drop_table("subject_term_results")

    op.drop_index(op.f("ix_assessment_components_school_id"), table_name="assessment_components")
    op.drop_table("assessment_components")

    # Now safe: subject_term_results (which held
    # fk_subject_term_result_student_term_record_school) is gone.
    op.drop_constraint("uq_student_term_record_id_school_id", "student_term_records", type_="unique")
    # Now safe: the unique constraint that covered school_id is gone, and
    # no remaining live FK on student_term_records references school_id
    # (all composite FKs on it were already dropped/replaced in STEP 3).
    op.drop_column("student_term_records", "school_id")
    # Now safe: assessment_components (which held
    # fk_assessment_component_term_school) is gone.
    op.drop_constraint("uq_academic_term_id_school_id", "academic_terms", type_="unique")
    # ### end Alembic commands ###
