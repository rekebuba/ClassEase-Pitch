from datetime import date, datetime
from decimal import Decimal
from typing import Any, Optional
from marshmallow import fields, ValidationError
from sqlalchemy import and_, or_

from api.v1.schemas.base_schema import get_all_model_classes
from models.base_model import CustomTypes
from werkzeug.datastructures import FileStorage


class FormattedDate(fields.Field):  # type: ignore[type-arg]
    """Custom field for formatting dates."""

    def __init__(
        self, format_str: str = "%b %d, %Y", *args: Any, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.format_str = format_str

    def _serialize(
        self,
        value: Any,
        attr: Optional[str],
        obj: Any,
        **kwargs: Any,
    ) -> str:
        if isinstance(value, datetime):
            return value.strftime(self.format_str)
        elif isinstance(value, str):
            try:
                dt = datetime.fromisoformat(value)
                return dt.strftime(self.format_str)
            except ValueError:
                return value  # fallback to original if parsing fails
        return None


class FloatOrDateField(fields.Field):  # type: ignore[type-arg]
    def _deserialize(
        self, value: Any, attr: Optional[str], data: Any, **kwargs: Any
    ) -> Any:
        if value is None:
            return None

        try:
            # Convert float (timestamp) to date if it's likely a date
            if isinstance(value, (int, float)) and value > 1e12:
                return datetime.fromtimestamp(value / 1000.0).date()
            # Otherwise treat as float
            return float(value)
        except (ValueError, TypeError):
            raise ValidationError("Invalid number or timestamp")

    def _serialize(
        self,
        value: Any,
        attr: Optional[str],
        obj: Any,
        **kwargs: Any,
    ) -> str:
        if isinstance(value, date):
            # Convert back to timestamp in milliseconds
            return int(datetime.combine(value, datetime.min.time()).timestamp() * 1000)
        elif isinstance(value, (int, float)):
            return value
        return None


class FileField(fields.Field):  # type: ignore[type-arg]
    """Custom field for file validation."""

    def _deserialize(
        self, value: Any, attr: Optional[str], data: Any, **kwargs: Any
    ) -> Any:
        if not isinstance(value, FileStorage):
            raise ValidationError("Invalid file type. Expected a file upload.")

        # Validate file size (e.g., 5MB limit)
        if value.content_length > 5 * 1024 * 1024:  # 5MB
            raise ValidationError("File size exceeds the 5MB limit.")

        # Validate file extension (allow only images)
        allowed_extensions = {"png", "jpg", "jpeg", "gif"}
        if not value.filename.lower().endswith(tuple(allowed_extensions)):
            raise ValidationError(
                "Invalid file type. Allowed extensions: png, jpg, jpeg, gif."
            )

        return value


class RoleEnumField(fields.Field):  # type: ignore[type-arg]
    """Custom field for RoleEnum."""

    def _serialize(
        self,
        value: Optional[CustomTypes.RoleEnum],
        attr: Optional[str],
        obj: Any,
        **kwargs: Any,
    ) -> str:
        """Custom serialization for RoleEnum."""
        if isinstance(value, CustomTypes.RoleEnum):
            return value.value.capitalize()  # Returns "Admin", "Teacher", or "Student"
        raise ValidationError("Expected RoleEnum instance")

    # runs when you call .load()
    def _deserialize(
        self, value: Any, attr: Optional[str], data: Any, **kwargs: Any
    ) -> Any:
        """Custom deserialization for RoleEnum."""
        try:
            if isinstance(value, CustomTypes.RoleEnum):
                return value
            return CustomTypes.RoleEnum(value.lower())  # Converts string to enum
        except ValueError as error:
            raise ValidationError(
                f"Invalid role. Must be one of: {[role.value for role in CustomTypes.RoleEnum]}"
            ) from error


class TableField(fields.Field):  # type: ignore[type-arg]
    def _deserialize(
        self, value: Any, attr: Optional[str], data: Any, **kwargs: Any
    ) -> Any:
        table_name = value.__tablename__.lower()
        table = get_all_model_classes().get(table_name)
        if not table:
            raise ValidationError(f"'{value}' is not a valid table.")

        return table


class TableIdField(fields.Field):  # type: ignore[type-arg]
    """Custom field for validating values."""

    def _validate(self, value: Any) -> None:
        if isinstance(value, str):
            return

        if isinstance(value, list):
            for item in value:
                if not (
                    isinstance(item, list)
                    and len(item) == 2
                    and all(isinstance(i, str) for i in item)
                ):
                    raise ValidationError(
                        "Each item in the list must be a list of two strings (like a tuple)",
                        field_name="value",
                    )
        else:
            raise ValidationError(
                "Value must be either a string or a list of two-item string lists.",
                field_name="value",
            )


class ColumnField(fields.Field):  # type: ignore[type-arg]
    """Custom field for validating values."""

    def _validate(self, value: Any) -> None:
        if not isinstance(value, (str, list)):
            raise ValidationError(
                "value must be either a string or a list", field_name="value"
            )


class JoinOperatorField(fields.Field):  # type: ignore[type-arg]
    def _deserialize(
        self, value: Any, attr: Optional[str], data: Any, **kwargs: Any
    ) -> Any:
        """Custom deserialization for join operator."""
        if isinstance(value, str):
            lowered = value.lower()
            if lowered == "and":
                return and_
            elif lowered == "or":
                return or_
        raise ValidationError("join_operator must be 'and' or 'or'")


class ValueField(fields.Field):  # type: ignore[type-arg]
    """Custom field for validating and deserializing various types of values."""

    # def _validate(self, value: Any) -> None:
    #     if not isinstance(value, (str, list, datetime, int, float)):
    #         raise ValidationError(
    #             "Value must be a string, list, datetime, int, or float.", field_name="value"
    #         )

    def _deserialize(
        self, value: Any, attr: Optional[str], data: Any, **kwargs: Any
    ) -> Any:
        if value is None:
            return None

        # If it's already a number, use it directly
        try:
            timestamp = float(value)
        except (ValueError, TypeError):
            return value  # Keep string or other types as-is

        try:
            # Consider values larger than 1e12 as millisecond timestamps
            if timestamp > 1e12:
                return datetime.fromtimestamp(timestamp / 1000.0).date()
            # If it's a regular float/int, return it
            return timestamp
        except (ValueError, OSError):
            raise ValidationError("Invalid numeric value or timestamp.")


class DecimalEncoder(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        # Ensure value is Decimal, round to 2 places, then convert to float
        return float(Decimal(str(value)).quantize(Decimal("0.00")))
