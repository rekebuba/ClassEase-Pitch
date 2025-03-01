from flask import request
from marshmallow import ValidationError
from models.admin import Admin
from models.user import User
from api.v1.services.base_user_service import BaseUserService
from models import storage
from api.v1.schemas.admin_schema import AdminSchema
from models import storage


class AdminService(BaseUserService):

    @staticmethod
    def get_admin_by_user_id(user_id: str) -> Admin:
        return Admin.query.filter_by(user_id=user_id).first()

    @staticmethod
    def get_admin_by_email(email: str) -> Admin | None:
        user = User.query.filter_by(email=email).first()
        if user:
            return Admin.query.filter_by(user_id=user.id).first()
        return None

    @classmethod
    def create_admin(cls, data) -> Admin:
        # Start a new transaction
        with storage.begin():
            user_data = {
                'image_path': request.files.get('image_path')
            }
            # Call the base class method to create a user with role 'admin'
            new_user = super().create_user(role='Admin', data=user_data)

            storage.session.add(new_user)
            storage.session.flush()  # Flush to get the new_user.id

            # Validate and create the Admin
            admin_schema = AdminSchema(session=storage.session)
            admin_data = {
                **data,
                'user_id': new_user.id
            }
            validated_admin_data = admin_schema.load(admin_data).to_dict()

            new_admin = Admin(**validated_admin_data)

            storage.session.add(new_admin)
            storage.session.commit()

        return new_admin

    @staticmethod
    def update_admin(admin: Admin, **kwargs) -> Admin:
        admin.update(**kwargs)
        return admin

    @staticmethod
    def delete_admin(admin: Admin) -> None:
        admin.delete()
