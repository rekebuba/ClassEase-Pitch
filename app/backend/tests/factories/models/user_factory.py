import os
import random
import tempfile
from io import BufferedReader
from typing import Any

from factory import LazyAttribute, RelatedFactory
from faker import Faker
from PIL import Image

from project.core.security import get_password_hash
from project.models.user import User
from project.utils.enum import RoleEnum
from tests.factories.typed_factory import TypedFactory

fake = Faker()


class UserFactory(TypedFactory[User]):
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

    student: Any = RelatedFactory(
        "tests.factories.models.student_factory.StudentFactory",
        factory_related_name="user",
    )

    role: Any = LazyAttribute(lambda x: random.choice(list(RoleEnum)))
    username = LazyAttribute(lambda x: str(fake.uuid4()))
    password: Any = LazyAttribute(lambda x: get_password_hash(x.username))
    image_path: Any = LazyAttribute(
        lambda x: UserFactory.generate_fake_profile_picture()
    )
