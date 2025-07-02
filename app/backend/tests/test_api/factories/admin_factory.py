from typing import Any, Dict
from factory import LazyAttribute
from faker import Faker
from models.admin import Admin
from models import storage
from .base_factory import BaseFactory
from .user_factory import UserFactory
from extension.enums.enum import RoleEnum

fake = Faker()


class AdminFactory(BaseFactory[Admin]):
    class Meta:
        model = Admin
        sqlalchemy_session = storage.session

    _add_for_session: Dict[str, Any] = {
        "user_id": lambda **kwarg: UserFactory.create(role=RoleEnum.ADMIN).id,
    }
    _add_for_test: Dict[str, Any] = {
        "user": lambda **kwarg: UserFactory.build(role=RoleEnum.ADMIN.value),
    }

    # Add additional fields for Admin
    first_name: Any = LazyAttribute(lambda x: fake.first_name())
    father_name: Any = LazyAttribute(lambda x: fake.last_name())
    grand_father_name: Any = LazyAttribute(lambda x: fake.first_name())
    date_of_birth: Any = LazyAttribute(lambda x: fake.date_of_birth())
    email: Any = LazyAttribute(lambda x: fake.email())
    gender: Any = LazyAttribute(lambda x: fake.random_element(elements=("M", "F")))
    phone: Any = LazyAttribute(lambda x: "091234567")
    address: Any = LazyAttribute(lambda x: fake.address())
