from datetime import date
from typing import Optional

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from project.core.security import get_password_hash
from project.models import (
    AuthIdentity,
    User,
)
from project.utils.enum import (
    AuthProviderEnum,
    GenderEnum,
    RoleEnum,
)


async def find_existing_user(
    session: AsyncSession,
    *,
    email: Optional[str] = None,
    phone: Optional[str] = None,
) -> Optional[User]:
    """
    Finds an existing user by email or phone.
    """
    if not email and not phone:
        return None

    filters = []
    if email:
        filters.append(User.email == email)
    if phone:
        filters.append(User.phone == phone)

    stmt = select(User).where(or_(*filters))
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_or_create_user(
    session: AsyncSession,
    *,
    first_name: str,
    father_name: str,
    grand_father_name: Optional[str],
    gender: GenderEnum,
    date_of_birth: date,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    role: RoleEnum = RoleEnum.STUDENT,
) -> User:
    """
    Gets an existing user or creates a new one with the provided profile information.
    """
    user = await find_existing_user(session, email=email, phone=phone)

    if user:
        # Update profile if it was empty
        if not user.first_name:
            user.first_name = first_name
            user.father_name = father_name
            user.grand_father_name = grand_father_name
            user.gender = gender
            user.date_of_birth = date_of_birth
        return user

    # Create new user
    user = User(
        first_name=first_name,
        father_name=father_name,
        grand_father_name=grand_father_name,
        gender=gender,
        date_of_birth=date_of_birth,
        email=email,
        phone=phone,
        username=username,
        is_active=True,  # Defaulting to active for now, can be adjusted
        is_verified=False,
    )
    session.add(user)
    await session.flush()

    if password:
        auth_identity = AuthIdentity(
            user_id=user.id,
            provider=AuthProviderEnum.PASSWORD,
            password=get_password_hash(password),
        )
        session.add(auth_identity)

    return user
