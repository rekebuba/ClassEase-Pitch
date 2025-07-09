import random
from typing import Any
from factory import LazyAttribute
from faker import Faker
from api.v1.views.admin.user.method import generate_id, hash_password
from api.v1.views.admin.user.schema import NewUserSchema
from extension.functions.helper import current_EC_year
from extension.enums.enum import RoleEnum
from tests.factories.api.typed_factory import TypedFactory

fake = Faker()


class NewUserFactory(TypedFactory[NewUserSchema]):
    class Meta:
        model = NewUserSchema

    role: Any = LazyAttribute(lambda x: random.choice(list(RoleEnum)))
    academic_id: Any = None
    image_path: Any = None
