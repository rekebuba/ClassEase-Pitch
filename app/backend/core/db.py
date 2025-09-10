from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from core.config import settings
from core.security import get_password_hash
from models.user import User
from utils.enum import RoleEnum

# Create the engine
engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI), future=True)
test_engine = create_engine(str(settings.TEST_SQLALCHEMY_DATABASE_URI), future=True)


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

        session.add(user_in)
        session.commit()
