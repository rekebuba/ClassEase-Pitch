from flask import request
from marshmallow import ValidationError
from models.student import Student
from models.user import User
from api.v1.services.base_user_service import BaseUserService
from api.v1.schemas.student_schema import StudentSchema
from models import storage
from models import storage


class StudentService(BaseUserService):
    @classmethod
    def create_student(cls, data) -> Student:
        # Start a new transaction
        with storage.begin():
            user_data = {
                'image_path': request.files.get('image_path')
            }
            # Call the base class method to create a user with role 'student'
            new_user = super().create_user(role='Student', data=user_data)

            storage.session.add(new_user)
            storage.session.flush()  # Flush to get the new_user.id

            # Validate and create the Student
            student_schema = StudentSchema(session=storage.session)
            student_data = {
                'name': data.get('name'),
                'email': data.get('email'),
                'user_id': new_user.id
            }
            validated_student_data = student_schema.load(
                student_data).to_dict()

            new_student = Student(**validated_student_data)

            storage.session.add(new_student)
            storage.session.commit()

        return new_student
