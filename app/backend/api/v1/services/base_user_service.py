from flask import request
from marshmallow import ValidationError
from api.v1.schemas.user_schema import UserSchema
from api.v1.views.methods import save_profile
from models.user import User
from models import storage
from models.admin import Admin
from api.v1.schemas.admin_schema import AdminSchema
from api.v1.schemas.student_schema import StudentSchema


class BaseUserService:
    """Base service for user-related operations."""

    @classmethod
    def create_user(cls, role, data):
        user_schema = UserSchema(session=storage.session)
        validated_user_data = user_schema.load(data).to_dict()

        # Save the profile picture if exists
        filepath = None
        if 'image_path' in validated_user_data and validated_user_data['image_path']:
            filepath = save_profile(validated_user_data['image_path'])
            validated_user_data['image_path'] = filepath

        # Create the user
        new_user = User(role=role, **validated_user_data)
        new_user.hash_password(new_user.id)

        return new_user

    @classmethod
    def create_role_based_user(cls, role, data) -> Admin | None:
        """Create a user with a specific role."""
        # Start a new transaction
        with storage.begin():
            user_data = {
                'image_path': request.files.get('image_path')
            }
            # Call the base class method to create a user with role 'admin'
            new_user = cls.create_user(role=role, data=user_data)

            storage.session.add(new_user)
            storage.session.flush()  # Flush to get the new_user.id

            fields = {
                **data,
                'user_id': new_user.id
            }
            if role == 'admin':
                # Validate and create the Admin
                admin_schema = AdminSchema(session=storage.session)
                validated_admin_data = admin_schema.load(fields).to_dict()

                new_admin = Admin(**validated_admin_data)

                storage.session.add(new_admin)
                storage.session.commit()
                return new_admin
            elif role == 'student':
                student_schema = StudentSchema(session=storage.session)
                validated_admin_data = student_schema.load(fields).to_dict()

                new_student = Admin(**validated_admin_data)

                storage.session.add(new_student)
                storage.session.commit()
                return new_student
            elif role == 'teacher':
                # Implement the teacher registration logic here
                pass

        return None
