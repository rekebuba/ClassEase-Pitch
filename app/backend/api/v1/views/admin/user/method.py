import random
import bcrypt
from sqlalchemy import select
from extension.enums.enum import RoleEnum
from models import storage
from models.user import User


def hash_password(v: str) -> str:
    return bcrypt.hashpw(v.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def generate_id(
    role: RoleEnum,
    academic_year: int,
    min_val: int = 1000,
    max_val: int = 9999,
    max_attempts: int = 100,
    base_sample_size: int = 5,
) -> str:
    """
    Generates a custom ID based on the role (Admin, Student, Teacher).

    Args:
        role: RoleEnum representing the user role (Admin, Student, Teacher)
        academic_year: Academic year as int (e.g., 2025)
        min_val: Minimum value of ID range (inclusive)
        max_val: Maximum value of ID range (inclusive)
        max_attempts: Maximum number of retries
        base_sample_size: Number of random samples to generate per attempt

    The ID format is: <section>/<random_number>/<year_suffix>
    - Section: 'MAS' for Student, 'MAT' for Teacher, 'MAA' for Admin
    - Random number: A 4-digit number between 1000 and 9999
    - Year suffix: Last 2 digits of the current Ethiopian year

    Returns:
        A unique identification string.

    Raises:
        ValueError: If a unique ID could not be generated in time.
    """
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

    sample_size = base_sample_size
    attempts = 0

    while attempts < max_attempts:
        random_ids = {random.randint(min_val, max_val) for _ in range(sample_size)}

        existing_ids = storage.session.scalars(
            select(User.identification).where(
                User.identification.in_(
                    [f"{section}/{rid}/{academic_year % 100}" for rid in random_ids]
                )
            )
        ).all()

        existing_rids = {
            int(id.split("/")[1])
            for id in existing_ids
            if id and "/" in id and len(id.split("/")) == 3
        }

        available_ids = random_ids - existing_rids
        if available_ids:
            chosen_id = random.choice(list(available_ids))
            return f"{section}/{chosen_id}/{academic_year % 100}"

        sample_size += base_sample_size
        attempts += 1

    raise ValueError(
        "Failed to generate a unique identification number after multiple attempts."
    )
