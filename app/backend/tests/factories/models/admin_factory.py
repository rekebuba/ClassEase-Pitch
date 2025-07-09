from typing import Any
from factory import LazyAttribute, SubFactory
from faker import Faker
from models.admin import Admin
from .base_factory import BaseFactory
from extension.enums.enum import RoleEnum, GenderEnum

fake = Faker()


class AdminFactory(BaseFactory[Admin]):
    class Meta:
        model = Admin
        exclude = ("user",)

    user: Any = SubFactory(
        "tests.factories.models.user_factory.UserFactory",
        role=RoleEnum.ADMIN,
        admin=None,
    )
    user_id: Any = LazyAttribute(lambda x: x.user.id if x.user else None)

    # Add additional fields for Admin
    first_name: Any = LazyAttribute(lambda x: fake.first_name())
    father_name: Any = LazyAttribute(lambda x: fake.last_name())
    grand_father_name: Any = LazyAttribute(lambda x: fake.first_name())
    date_of_birth: Any = LazyAttribute(lambda x: fake.date_of_birth())
    email: Any = LazyAttribute(lambda x: fake.email())
    gender: Any = LazyAttribute(
        lambda x: fake.random_element(elements=list(GenderEnum))
    )
    phone: Any = LazyAttribute(lambda x: "091234567")
    address: Any = LazyAttribute(lambda x: fake.address())
