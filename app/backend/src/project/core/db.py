import redis
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from project.core.config import settings
from project.core.security import get_password_hash
from project.models import AuthIdentity
from project.models.admin import Admin
from project.models.user import User
from project.utils.enum import AuthProviderEnum, RoleEnum

# Create the engine
engine = create_engine(str(settings.SQLALCHEMY_POSTGRES_DATABASE_URI), future=True)
redis_client = redis.asyncio.Redis.from_url(
    str(settings.REDIS_URL), decode_responses=True
)


def init_db(session: Session) -> None:
    """Initialize the database with first super user."""
    user = session.execute(
        select(User).where(User.username == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        hash_password = get_password_hash(settings.FIRST_SUPERUSER_PASSWORD)
        user = User(
            username=settings.FIRST_SUPERUSER,
            role=RoleEnum.ADMIN,
            email=settings.FIRST_SUPERUSER_EMAIL,
            phone=settings.FIRST_SUPERUSER_PHONE,
            is_active=True,
            is_verified=True,
        )

        session.add(user)
        session.flush()

        provider = AuthIdentity(
            user_id=user.id,
            provider=AuthProviderEnum.PASSWORD,
            password=hash_password,
        )

        admin = Admin(
            user_id=user.id,
            first_name=settings.FIRST_SUPERUSER_NAME,
            father_name=settings.FIRST_SUPERUSER_FATHER_NAME,
            grand_father_name=settings.FIRST_SUPERUSER_GRAND_FATHER_NAME,
            date_of_birth=settings.FIRST_SUPERUSER_DATE_OF_BIRTH,
            gender=settings.FIRST_SUPERUSER_GENDER,
        )

        session.add(admin)
        session.add(provider)
        session.commit()
