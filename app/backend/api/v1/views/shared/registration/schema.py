from api.v1.schemas.base_schema import BaseSchema
from api.v1.schemas.custom_schema import RoleEnumField
from marshmallow import fields



class UserSchema(BaseSchema):
    """
    Schema for user details.
    """

    id = fields.String(dump_only=True)
    role = RoleEnumField()


class DumpResultSchema(BaseSchema):
    """
    Schema for successful registration response.
    """

    message = fields.String(dump_only=True)
    user = fields.Nested(UserSchema, dump_only=True)
