from marshmallow import Schema, ValidationError, fields, pre_load, validates, validates_schema
from api.v1.schemas.base_schema import BaseSchema
from api.v1.schemas.semester.create_schema import SemesterCreationSchema


class EventCreationSchema(BaseSchema):
    """Schema for validating event creation data."""
    title = fields.String(required=True, validate=[
                          fields.validate.Length(min=3, max=100)])
    purpose = fields.String(required=True, validate=lambda x: x in [
                            'New Semester', 'Graduation', 'Sports Event', 'Administration', 'Other'])
    organizer = fields.String(required=True, validate=lambda x: x in [
                              'School Administration', 'School', 'Student Club', 'External Organizer'])

    ethiopian_year = fields.String(required=True)
    gregorian_year = fields.String(required=False, allow_none=True, load_default=None)

    start_date = fields.Date(required=True, format='iso')
    end_date = fields.Date(required=True, format='iso')
    start_time = fields.DateTime(load_default=None, format='%H:%M:%S')
    end_time = fields.DateTime(load_default=None, format='%H:%M:%S')

    location_type = fields.String(load_default=None, validate=lambda x: x in [
                                  'Auditorium', 'Classroom', 'Sports Field', 'Online', 'Other'])
    is_hybrid = fields.Boolean(load_default=None)
    online_link = fields.Url(load_default=None)

    requires_registration = fields.Boolean(load_default=None)
    registration_start = fields.Date(load_default=None, format='iso')
    registration_end = fields.Date(load_default=None, format='iso')

    eligibility = fields.String(load_default=None, validate=lambda x: x in [
                                'All', 'Students Only', 'Faculty Only', 'Invitation Only'])
    has_fee = fields.Boolean(load_default=None)
    fee_amount = fields.Float(load_default=None, validate=[
                              fields.validate.Range(min=0)])

    description = fields.String(load_default=None)

    semester = fields.Nested(
        SemesterCreationSchema, required=True, load_only=True, exclude=("event_id",))

    message = fields.String(dump_only=True)

    @pre_load
    def set_defaults(self, data, **kwargs):
        # add default values for ethiopian_year and gregorian_year
        data['gregorian_year'] = self.current_GC_year(int(data['ethiopian_year']))
        return data

    @validates_schema
    def validate_dates_and_times(self, data, **kwargs):
        """Ensure start_date is before end_date and start_time is before end_time."""
        try:
            if data["start_date"] > data["end_date"]:
                raise ValidationError(
                    "Start date cannot be after end date.", "start_date")
            if data["start_time"] > data["end_time"]:
                raise ValidationError(
                    "Start time cannot be after end time.", "start_time")
            if data['registration_start'] > data['registration_end']:
                raise ValidationError(
                    "Registration start date cannot be after registration end date.")
            if data['location_type'] == 'Online' and not data['online_link']:
                raise ValidationError(
                    "Online link is required for online events.")
            if data['requires_registration'] and not data['registration_start'] and not data['registration_end']:
                raise ValidationError(
                    "Registration dates are required for events that require registration.")
            if data['has_fee'] and data['fee_amount'] <= 0:
                raise ValidationError(
                    "Fee amount is required for events that have a fee.")
            if data['is_hybrid'] and data['location_type'] != 'Online':
                raise ValidationError(
                    "Hybrid events must have an online location type.")
            if data['purpose'] == 'New Semester' and data['organizer'] != 'School Administration':
                raise ValidationError(
                    "New semester events must be organized by the school administration.")
            if data['purpose'] == 'New Semester' and data['location_type'] != 'Online':
                raise ValidationError(
                    "New semester events must have an online location type.")
            if data['purpose'] == 'New Semester' and not data['is_hybrid']:
                raise ValidationError("New semester events must be hybrid.")
            if data['purpose'] == 'New Semester' and not data['has_fee']:
                raise ValidationError("New semester events must have a fee.")
            if data['purpose'] == 'New Semester' and not data['requires_registration']:
                raise ValidationError(
                    "New semester events must require registration.")
            if data['purpose'] == 'New Semester' and data['eligibility'] != 'All':
                raise ValidationError(
                    "New semester events must be open to all.")
            if data['purpose'] == 'New Semester' and data['fee_amount'] == 0.00:
                raise ValidationError("New semester events must have a fee.")
        except TypeError:
            print('this is why')
            pass
