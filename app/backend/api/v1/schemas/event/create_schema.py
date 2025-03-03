from marshmallow import Schema, fields
from api.v1.schemas.base_schema import BaseSchema


class EventCreationSchema(BaseSchema):
    """Schema for validating event creation data."""
    event_name = fields.String(required=True)
    purpose = fields.String(required=True)
    organizer = fields.String(required=True)

    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    start_time = fields.DateTime(required=False)
    end_time = fields.DateTime(required=False)

    location_type = fields.String(required=False, validate=lambda x: x in ['Auditorium', 'Classroom', 'Sports Field', 'Online', 'Other'])
    is_hybrid = fields.Boolean(required=False)
    online_link = fields.String(required=False)

    requires_registration = fields.Boolean(required=False)
    registration_start = fields.Date(required=False)
    registration_end = fields.Date(required=False)

    eligibility = fields.String(required=False, validate=lambda x: x in ['All', 'Students Only', 'Faculty Only', 'Invitation Only'])
    has_fee = fields.Boolean(required=False)
    fee_amount = fields.Float(required=False)

    description = fields.String(required=False)
