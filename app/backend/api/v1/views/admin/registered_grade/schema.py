from api.v1.schemas.base_schema import BaseSchema
from marshmallow import fields


class RegisteredGradesSchema(BaseSchema):
    grades = fields.List(fields.Integer, required=True)
