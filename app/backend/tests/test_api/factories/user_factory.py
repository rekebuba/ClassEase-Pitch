import os
import random
import tempfile
from typing import Any, Dict, List
import bcrypt
from factory import LazyAttribute
from faker import Faker
from pyethiodate import EthDate
from datetime import datetime
from io import BufferedReader
from PIL import Image
from models.user import User
from models import storage
from .base_factory import BaseFactory
from extension.enums.enum import RoleEnum

fake = Faker()


class UserFactory(BaseFactory[User]):
    class Meta:
        model = User
        sqlalchemy_session = storage.session

    _add_for_test: Dict[str, Any] = {}
    _add_for_session: Dict[str, Any] = {
        "identification.role.count": lambda **kwarg: UserFactory._generate_id(
            kwarg["role"], kwarg["count"]
        ),
        "password.identification": lambda **kwarg: UserFactory._hash_password(
            kwarg["identification"]
        ),
    }
    _skip_fields: List[str] = ["count"]

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

    @staticmethod
    def _generate_id(role: "RoleEnum", count: int) -> str:
        """
        Generates a custom ID based on the role (Admin, Student, Teacher).

        The ID format is: <section>/<random_number>/<year_suffix>
        - Section: 'MAS' for Student, 'MAT' for Teacher, 'MAA' for Admin
        - Random number: A 4-digit number between 1000 and 9999
        - Year suffix: Last 2 digits of the current Ethiopian year
        """
        identification: str = ""
        section: str = ""

        # Assign prefix based on role
        if role == RoleEnum.STUDENT:
            section = "MAS"
        elif role == RoleEnum.TEACHER:
            section = "MAT"
        elif role == RoleEnum.ADMIN:
            section = "MAA"
        else:
            raise ValueError(f"Invalid role: {role}")

        starting_year: int = (
            EthDate.date_to_ethiopian(datetime.now()).year % 100
        )  # Get last 2 digits of the year
        identification = f"{section}/{count}/{starting_year}"

        return identification

    @staticmethod
    def _hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    count: Any = LazyAttribute(
        lambda x: fake.random_int()
    )  # Unique identifier for each user, starting at 1000

    image_path: Any = LazyAttribute(
        lambda x: UserFactory.generate_fake_profile_picture()
    )
    national_id: Any = LazyAttribute(lambda x: str(fake.uuid4()))
    role: Any = LazyAttribute(lambda x: random.choice(list(RoleEnum)))
