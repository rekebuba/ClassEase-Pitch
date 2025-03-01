from marshmallow import fields
from marshmallow import ValidationError, validates_schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from api.v1.schemas.base_schema import BaseSchema
from models.user import User
from werkzeug.datastructures import FileStorage
from models import storage

class FileField(fields.Field):
    """Custom field for file validation."""

    def _deserialize(self, value, attr, data, **kwargs):
        if not isinstance(value, FileStorage):
            raise ValidationError("Invalid file type. Expected a file upload.")

        # Validate file size (e.g., 5MB limit)
        if value.content_length > 5 * 1024 * 1024:  # 5MB
            raise ValidationError("File size exceeds the 5MB limit.")

        # Validate file extension (allow only images)
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        if not value.filename.lower().endswith(tuple(allowed_extensions)):
            raise ValidationError(
                "Invalid file type. Allowed extensions: png, jpg, jpeg, gif.")

        return value


class UserSchema(BaseSchema, SQLAlchemyAutoSchema):
    class Meta:
        model = User
        sqla_session = storage.session  # Provide the SQLAlchemy session
        load_instance = True
        exclude = ('id', 'password')

    identification = fields.UUID(dump_only=True)
    role = fields.String(required=False)
    image_path = FileField(required=False)
