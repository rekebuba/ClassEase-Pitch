from marshmallow import fields, ValidationError
from sqlalchemy import and_, or_

from api.v1.schemas.base_schema import get_all_model_classes
from models.base_model import CustomTypes
from werkzeug.datastructures import FileStorage


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


class RoleEnumField(fields.Field):
    """Custom field for RoleEnum."""

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return value.value.capitalize()  # Returns "Admin", "Teacher", or "Student"

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            if isinstance(value, CustomTypes.RoleEnum):
                return value
            return CustomTypes.RoleEnum(value)  # Converts string to enum
        except ValueError as error:
            raise ValidationError(
                "Invalid role. Must be one of: admin, teacher, student") from error


class TableField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        table_name = value.__tablename__.lower()
        table = get_all_model_classes().get(table_name)
        if not table:
            raise ValidationError(f"'{value}' is not a valid table.")

        return table


class TableIdField(fields.Field):
    """Custom field for validating values."""

    def _validate(self, value):
        if isinstance(value, str):
            return

        if isinstance(value, list):
            for item in value:
                if not (isinstance(item, list) and len(item) == 2 and all(isinstance(i, str) for i in item)):
                    raise ValidationError(
                        "Each item in the list must be a list of two strings (like a tuple)",
                        field_name="value"
                    )
        else:
            raise ValidationError(
                "Value must be either a string or a list of two-item string lists.",
                field_name="value"
            )


class ColumnField(fields.Field):
    """Custom field for validating values."""

    def _validate(self, value):
        if not isinstance(value, (str, list)):
            raise ValidationError(
                "value must be either a string or a list", field_name="value"
            )
        return value


class JoinOperatorField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, str):
            lowered = value.lower()
            if lowered == 'and':
                return and_
            elif lowered == 'or':
                return or_
        raise ValidationError("join_operator must be 'and' or 'or'")


class ValueField(fields.Field):
    """Custom field for validating values."""

    def _validate(self, value):
        if not isinstance(value, (str, list)):
            raise ValidationError(
                "value must be either a string or a list", field_name="value"
            )
        return value
