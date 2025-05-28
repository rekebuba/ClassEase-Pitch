from api.v1.schemas.base_schema import BaseSchema
from api.v1.schemas.schemas import FullNameSchema
from api.v1.views.shared.registration.schema import UserSchema
from marshmallow import fields


class UserDetailSchema(BaseSchema):
    user = fields.Nested(UserSchema(only=("identification", "imagePath", "role")))
    detail = fields.Nested(FullNameSchema)
