from typing import Tuple

from flask import Response, jsonify, request
from sqlalchemy import and_, select, true, update
from api.v1.utils.typing import UserT
from api.v1.views.utils import admin_required
from models.assessment import Assessment
from models.average_subject import AVRGSubject
from models.grade import Grade
from models.mark_list import MarkList
from models.section import Section
from models.subject import Subject
from models.teacher import Teacher
from models.teacher_record import TeachersRecord
from api.v1.views.admin import admins as admin
from models import storage


@admin.route("/assign-teacher", methods=["PUT"])
@admin_required
def assign_class(admin_data: UserT) -> Tuple[Response, int]:
    """
    Assigns a teacher to a class based on the provided data.

    Args:
        admin_data (dict): Data containing information about the teacher and class assignment.

    Returns:
        Response: JSON response indicating success or failure of the operation.
    """
    data = request.get_json()
    if not data:
        return jsonify({"message": "Not a JSON"}), 400

    required_data = [
        "teacher_id",
        "grade",
        "section",
        "subjects_taught",
        "semester",
        "mark_list_year",
    ]
    # Check if required fields are present
    for field in required_data:
        if field not in data:
            return jsonify({"message": f"Missing {field}"}), 400

    # Get the teacher by ID
    teacher = storage.get_first(Teacher, id=data["teacher_id"])
    if not teacher:
        return jsonify({"message": "Teacher not found"}), 404

    # Get the grade_id from the Grade table
    grade_id = (
        storage.session.execute(select(Grade.id).where(Grade.grade == data["grade"]))
        .scalars()
        .first()
    )
    if not grade_id:
        return jsonify({"message": "No grade found for the teacher"}), 404

    # get the subject_id
    subjects_taught = (
        storage.session.query(Subject)
        .filter(Subject.grade_id == grade_id, Subject.name.in_(data["subjects_taught"]))
        .all()
    )
    if not subjects_taught:
        return jsonify({"message": "Subject not found"}), 404

    try:
        for subject in subjects_taught:
            # get the section_id
            section_ids = [
                id[0]
                for id in storage.session.query(Section.id)
                .filter(
                    Section.grade_id == grade_id, Section.section.in_(data["section"])
                )
                .all()
            ]

            if not section_ids:
                return jsonify(
                    {
                        "message": f"Section not found, Mark List was not created for the grade {data['grade']}"
                    }
                ), 404

            for section_id in section_ids:
                # check if the another teacher is already assigned to the subject
                teacher_record = storage.get_first(
                    TeachersRecord,
                    grade_id=grade_id,
                    section_id=section_id,
                    subject_id=subject.id,
                    semester=data["semester"],
                )
                # update the teacher record
                if teacher_record:
                    return jsonify({"message": "Teacher already assigned"}), 409
                teacher_record = TeachersRecord(
                    teacher_id=teacher.id,
                    grade_id=grade_id,
                    section_id=section_id,
                    subject_id=subject.id,
                    semester=data["semester"],
                )

                storage.add(teacher_record)

                # Update the MarkList table
                storage.session.execute(
                    update(MarkList)
                    .where(
                        and_(
                            MarkList.grade_id == grade_id,
                            MarkList.section_id == section_id,
                            MarkList.subject_id == subject.id,
                            MarkList.semester == data["semester"],
                            MarkList.year == data["mark_list_year"],
                        )
                    )
                    .values(teachers_record_id=teacher_record.id)
                )

                # Update the Assessment table
                storage.session.execute(
                    update(Assessment)
                    .where(
                        and_(
                            true(),
                            Assessment.grade_id == grade_id,
                            Assessment.subject_id == subject.id,
                            Assessment.semester == data["semester"],
                            Assessment.year == data["mark_list_year"],
                        )
                    )
                    .values(teachers_record_id=teacher_record.id)
                )

                # Update the AVRGSubject table
                storage.session.execute(
                    update(AVRGSubject)
                    .where(
                        and_(
                            AVRGSubject.grade_id == grade_id,
                            AVRGSubject.subject_id == subject.id,
                            AVRGSubject.year == data["mark_list_year"],
                        )
                    )
                    .values(teachers_record_id=teacher_record.id)
                )

                # Commit the final updates to the database
                storage.save()
    except Exception:
        storage.rollback()
        return jsonify({"message": "error internal server"}), 500

    return jsonify({"message": "Teacher assigned successfully!"}), 201
