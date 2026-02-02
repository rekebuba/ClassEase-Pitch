from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from core.config import settings
from core.security import get_password_hash
from models.admin import Admin
from models.user import User
from utils.enum import RoleEnum

# Create the engine
engine = create_engine(str(settings.SQLALCHEMY_POSTGRES_DATABASE_URI), future=True)


def init_db(session: Session) -> None:
    """Initialize the database with first super user."""

    user = session.execute(
        select(User).where(User.identification == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        hash_password = get_password_hash(settings.FIRST_SUPERUSER_PASSWORD)
        user_in = User(
            identification=settings.FIRST_SUPERUSER,
            password=hash_password,
            role=RoleEnum.ADMIN,
        )
        admin = Admin(
            user_id=user_in.id,
            first_name=settings.FIRST_SUPERUSER_NAME,
            father_name=settings.FIRST_SUPERUSER_FATHER_NAME,
            grand_father_name=settings.FIRST_SUPERUSER_GRAND_FATHER_NAME,
            date_of_birth=settings.FIRST_SUPERUSER_DATE_OF_BIRTH,
            gender=settings.FIRST_SUPERUSER_GENDER,
            email=settings.FIRST_SUPERUSER_EMAIL,
            phone=settings.FIRST_SUPERUSER_PHONE,
            address=settings.FIRST_SUPERUSER_ADDRESS,
        )

        session.add(user_in)
        session.add(admin)
        session.commit()
