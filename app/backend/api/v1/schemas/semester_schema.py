from marshmallow import Schema, ValidationError, fields, validates
from api.v1.schemas.base_schema import BaseSchema
from models import storage
from models.event import Event


class SemesterCreationSchema(BaseSchema):
    """Schema for validating semester creation data."""
    event_id = fields.String(required=True, load_only=True)
    name = fields.Integer(required=True, load_only=True, validate=[
                          fields.validate.Range(min=1, max=2)])

    @validates('event_id')
    def valid_event_id(self, event_id):
        if not storage.session.query(Event).filter_by(id=event_id).first():
            raise ValidationError('Event Was Not Created Successfully.')
