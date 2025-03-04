from marshmallow import Schema, ValidationError, fields, validates
from api.v1.schemas.base_schema import BaseSchema
from api.v1.schemas.semester.create_schema import SemesterCreationSchema


class EventCreationSchema(BaseSchema):
    """Schema for validating event creation data."""
    event_name = fields.String(required=True, validate=[fields.Length(max=3)])
    purpose = fields.String(required=True, validate=lambda x: x in [
                            'New Semester', 'Graduation', 'Sports Event', 'Administration', 'Other'])
    organizer = fields.String(required=True, validate=lambda x: x in [
                              'School Administration', 'School', 'Student Club', 'External Organizer'])

    start_date = fields.Date(required=True, validate=[fields.Date('iso')])
    end_date = fields.Date(required=True, validate=[fields.Date('iso')])
    start_time = fields.DateTime(required=False, validate=[
                                 fields.Time('iso')])
    end_time = fields.DateTime(required=False, validate=[fields.Time('iso')])

    location_type = fields.String(required=False, validate=lambda x: x in [
                                  'Auditorium', 'Classroom', 'Sports Field', 'Online', 'Other'])
    is_hybrid = fields.Boolean(required=False)
    online_link = fields.Url(required=False)

    requires_registration = fields.Boolean(required=False)
    registration_start = fields.Date(required=False, validate=[fields.Date('iso')])
    registration_end = fields.Date(required=False, validate=[fields.Date('iso')])

    eligibility = fields.String(required=False, validate=lambda x: x in [
                                'All', 'Students Only', 'Faculty Only', 'Invitation Only'])
    has_fee = fields.Boolean(required=False)
    fee_amount = fields.Float(required=False, validate=[fields.validate.Range(min=0)])

    description = fields.String(required=False)

    semester = fields.Nested(SemesterCreationSchema, required=False)

    @validates('start_date')
    def validate_start_date(self, value):
        """Validate start date."""
        if value > self.end_date:
            raise ValidationError("Start date cannot be after end date.")

    @validates('start_time')
    def validate_start_time(self, value):
        """Validate start time."""
        if value > self.end_time:
            raise ValidationError("Start time cannot be after end time.")

    @validates('registration_start')
    def validate_registration_start(self, value):
        """Validate registration start date."""
        if value > self.registration_end:
            raise ValidationError(
                "Registration start date cannot be after registration end date.")

    @validates('online_link')
    def validate_online_link(self, value):
        """Validate online link."""
        if self.location_type == 'Online' and not value:
            raise ValidationError("Online link is required for online events.")

    @validates('requires_registration')
    def validate_registration(self, value):
        """Validate registration."""
        if value and not self.registration_start and not self.registration_end:
            raise ValidationError(
                "Registration dates are required for events that require registration.")

    @validates('has_fee')
    def validate_fee(self, value):
        """Validate fee."""
        if value and self.fee_amount <= 0:
            raise ValidationError(
                "Fee amount is required for events that have a fee.")

    @validates('eligibility')
    def validate_eligibility(self, value):
        """Validate eligibility."""
        if value == 'Invitation Only' and not self.requires_registration:
            raise ValidationError(
                "Events that are invitation only must require registration.")

    @validates('is_hybrid')
    def validate_hybrid(self, value):
        """Validate hybrid."""
        if value and self.location_type != 'Online':
            raise ValidationError(
                "Hybrid events must have an online location type.")

    @validates('location_type')
    def validate_location_type(self, value):
        """Validate location type."""
        if self.is_hybrid and value != 'Online':
            raise ValidationError(
                "Hybrid events must have an online location type.")

    @validates('purpose')
    def validate_purpose(self, value):
        """Validate purpose."""
        if value == 'New Semester' and self.organizer != 'School Administration':
            raise ValidationError("New semester events must be organized by the school administration.")
        if value == 'New Semester' and self.location_type != 'Online':
            raise ValidationError("New semester events must have an online location type.")
        if value == 'New Semester' and not self.has_fee:
            raise ValidationError("New semester events must have a fee.")
        if value == 'New Semester' and not self.requires_registration:
            raise ValidationError("New semester events must require registration.")
        if value == 'New Semester' and self.eligibility != 'All':
            raise ValidationError("New semester events must be open to all.")
        if value == 'New Semester' and not self.is_hybrid:
            raise ValidationError("New semester events must be hybrid.")
        if value == 'New Semester' and self.fee_amount == 0:
            raise ValidationError("New semester events must have a fee.")
