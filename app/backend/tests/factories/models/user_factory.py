import os
import random
import tempfile
from typing import Any
from factory import LazyAttribute, SubFactory, RelatedFactory
from faker import Faker
from io import BufferedReader
from PIL import Image
from api.v1.views.admin.user.method import generate_id, hash_password
from extension.functions.helper import current_EC_year
from models.user import User
from .base_factory import BaseFactory
from extension.enums.enum import RoleEnum

fake = Faker()


class UserFactory(BaseFactory[User]):
    class Meta:
        model = User
        exclude = ("admin", "teacher", "student")

    @staticmethod
    def generate_fake_profile_picture() -> BufferedReader:
        directory = "profiles"
        os.makedirs(directory, exist_ok=True)  # Ensure directory exists

        # Create a random image using Pillow
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=True) as tmp:
            # Generate and save image
            image = Image.new(
                "RGB",
                (256, 256),
                (
                    fake.random_int(0, 255),
                    fake.random_int(0, 255),
                    fake.random_int(0, 255),
                ),
            )
            image.save(tmp.name, format="JPEG")

            # Reopen in binary mode and return (file will auto-delete when closed)
            return open(tmp.name, "rb")

    admin: Any = RelatedFactory(
        "tests.factories.models.admin_factory.AdminFactory",
        factory_related_name="user",
    )
    student: Any = RelatedFactory(
        "tests.factories.models.teacher_factory.TeacherFactory",
        factory_related_name="user",
    )
    teacher: Any = RelatedFactory(
        "tests.factories.models.student_factory.StudentFactory",
        factory_related_name="user",
    )

    role: Any = LazyAttribute(lambda x: random.choice(list(RoleEnum)))
    identification: Any = LazyAttribute(
        lambda x: generate_id(x.role, current_EC_year())
    )
    password: Any = LazyAttribute(lambda x: hash_password(x.identification))
    image_path: Any = LazyAttribute(
        lambda x: UserFactory.generate_fake_profile_picture()
    )
