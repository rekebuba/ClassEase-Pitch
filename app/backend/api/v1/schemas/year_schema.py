from marshmallow import fields, pre_load
from api.v1.schemas.base_schema import BaseSchema
from models import storage
from models.year import Year


class yearValidationSchema(BaseSchema):
    """Schema for validating Year"""
    academic_year = fields.Integer(required=True, load_only=True)
    year_id = fields.String(dump_only=True, load_default=None)

    @pre_load
    def set_defaults(self, data, **kwargs):
        year_id = storage.session.query(Year.id).filter_by(
            ethiopian_year=data.get('academic_year')
        ).scalar()

        if year_id is not None:
            data['year_id'] = year_id
        return data
