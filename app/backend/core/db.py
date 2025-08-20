# app/core/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from core.config import settings
from models.base.base_model import Base

# Create the engine
engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI), future=True, echo=True)

# Session factory
SessionLocal = sessionmaker(
    bind=engine, autoflush=False, autocommit=False, expire_on_commit=False
)


# Dependency for FastAPI
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Optional: init tables + seed data
def init_db() -> None:
    Base.metadata.create_all(bind=engine)

    from models.ceo import seed_ceo  # noqa: F401
    from models.table import seed_table  # noqa: F401

    with SessionLocal() as session:
        seed_ceo(session)
        seed_table(session, engine)
