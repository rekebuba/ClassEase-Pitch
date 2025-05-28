from typing import Any, Dict
from api.v1.schemas.base_schema import BaseSchema
from marshmallow import (
    ValidationError,
    validate,
    post_dump,
    pre_load,
    validates,
    validates_schema,
    fields,
)
from models.year import Year
from models import storage
from models.event import Event


class SemesterCreationSchema(BaseSchema):
    """Schema for validating semester creation data."""

    event_id = fields.String(required=True, load_only=True)
    name = fields.Integer(
        required=True, load_only=True, validate=[validate.Range(min=1, max=2)]
    )

    @validates("event_id")
    def valid_event_id(self, event_id: str) -> None:
        if not storage.session.query(Event.id).filter_by(id=event_id).scalar():
            raise ValidationError("Event Was Not Created Successfully.")


class EventSchema(BaseSchema):
    """Schema for validating event creation data."""

    title = fields.String(required=True, validate=[validate.Length(min=3, max=100)])
    purpose = fields.String(
        required=True,
        validate=lambda x: x
        in ["New Semester", "Graduation", "Sports Event", "Administration", "Other"],
    )
    organizer = fields.String(
        required=True,
        validate=lambda x: x
        in ["School Administration", "School", "Student Club", "External Organizer"],
    )

    academic_year = fields.Integer(validate=[validate.Range(min=2000, max=2100)])

    year_id = fields.String(required=False, load_default=None)

    start_date = fields.Date(required=True, format="iso")
    end_date = fields.Date(required=True, format="iso")
    start_time = fields.DateTime(load_default=None, format="%H:%M:%S")
    end_time = fields.DateTime(load_default=None, format="%H:%M:%S")

    location = fields.String(
        load_default=None,
        validate=lambda x: x
        in ["Auditorium", "Classroom", "Sports Field", "Online", "Other"],
    )
    is_hybrid = fields.Boolean(load_default=False, load_only=True)
    online_link = fields.Url(load_default=None)

    requires_registration = fields.Boolean(load_default=False, load_only=True)
    registration_start = fields.Date(load_default=None, format="iso")
    registration_end = fields.Date(load_default=None, format="iso")

    eligibility = fields.String(
        load_default=None,
        validate=lambda x: x
        in ["All", "Students Only", "Faculty Only", "Invitation Only"],
    )
    has_fee = fields.Boolean(load_default=False)
    fee_amount = fields.Float(load_default=None, validate=[validate.Range(min=0)])

    description = fields.String(load_default=None)

    semester = fields.Nested(
        SemesterCreationSchema, load_only=True, exclude=("event_id",)
    )

    message = fields.String(dump_only=True)

    @pre_load
    def set_defaults(self, data: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
        # add default values to the data
        data["year_id"] = self.get_year_id(data.pop("academic_year", None))

        return data

    @validates_schema
    def validate_dates_and_times(self, data: Dict[str, Any], **kwargs: Any) -> None:
        """Ensure start_date is before end_date and start_time is before end_time."""
        try:
            if data["start_date"] and data["end_date"]:
                if data["start_date"] > data["end_date"]:
                    raise ValidationError(
                        "Start date cannot be after end date.", "start_date"
                    )
            if data["start_time"] and data["end_time"]:
                if data["start_time"] > data["end_time"]:
                    raise ValidationError(
                        "Start time cannot be after end time.", "start_time"
                    )
            if data["registration_start"] and data["registration_end"]:
                if data["registration_start"] > data["registration_end"]:
                    raise ValidationError(
                        "Registration start date cannot be after registration end date."
                    )
            if (
                data["requires_registration"]
                and not data["registration_start"]
                and not data["registration_end"]
            ):
                raise ValidationError(
                    "Registration dates are required for events that require registration."
                )
            if data["has_fee"] and data["fee_amount"] <= 0:
                raise ValidationError(
                    "Fee amount is required for events that have a fee."
                )
            if data["is_hybrid"] and data["online_link"] is None:
                raise ValidationError("Online link is required for hybrid events.")
            if (
                data["purpose"] == "New Semester"
                and data["organizer"] != "School Administration"
            ):
                raise ValidationError(
                    "New semester events must be organized by the school administration."
                )
            if data["purpose"] == "New Semester" and data["location"] != "Online":
                raise ValidationError(
                    "New semester events must have an online location type."
                )
            if data["purpose"] == "New Semester" and not data["has_fee"]:
                raise ValidationError("New semester events must have a fee.")
            if data["purpose"] == "New Semester" and not data["requires_registration"]:
                raise ValidationError("New semester events must require registration.")
            if data["purpose"] == "New Semester" and data["eligibility"] != "All":
                raise ValidationError("New semester events must be open to all.")
            if data["purpose"] == "New Semester" and data["fee_amount"] == 0.00:
                raise ValidationError("New semester events must have a fee.")
        except TypeError as e:
            raise e

    @post_dump
    def add_academic_year(self, data, **kwargs: Any):
        year = (
            storage.session.query(Year.ethiopian_year, Year.gregorian_year)
            .filter(Year.id == data.get("year_id"))
            .first()
        )
        if year:
            ethiopian_year, gregorian_year = year
            parts = gregorian_year.split("/")
            # to get the last two digits of the year (e.g., 2021/2022 -> 2021/22)
            updated_gregorian_year = f"{parts[0]}/{parts[1][-2:]}"

            data["academic_year"] = f"{ethiopian_year} ({updated_gregorian_year})"

        return data


class AvailableEventsSchema(BaseSchema):
    events = fields.List(
        fields.Nested(
            EventSchema,
            exclude=(
                "start_time",
                "end_time",
                "registration_start",
                "registration_end",
                "fee_amount",
                "description",
                "message",
            ),
        ),
        required=True,
    )
