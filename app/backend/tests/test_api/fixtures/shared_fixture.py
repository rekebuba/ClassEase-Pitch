from typing import Iterator, List
from flask.testing import FlaskClient
import pytest
from sqlalchemy import select

from extension.pydantic.models.grade_schema import GradeSchema
from extension.pydantic.models.section_schema import SectionSchema
from extension.pydantic.models.stream_schema import StreamSchema
from extension.pydantic.models.subject_schema import SubjectSchema
from models.grade import Grade
from models.section import Section
from models.stream import Stream
from models.subject import Subject
from models import storage


@pytest.fixture(scope="session")
def subjects(client: FlaskClient) -> Iterator[List[SubjectSchema]]:
    subjects = storage.session.scalars(select(Subject)).all()
    subjects_schemas = [SubjectSchema.model_validate(subject) for subject in subjects]
    yield subjects_schemas


@pytest.fixture(scope="session")
def grades(client: FlaskClient) -> Iterator[List[GradeSchema]]:
    grades = storage.session.scalars(select(Grade)).all()
    grades_schemas = [GradeSchema.model_validate(grade) for grade in grades]
    yield grades_schemas


@pytest.fixture(scope="session")
def sections(client: FlaskClient) -> Iterator[List[SectionSchema]]:
    sections = storage.session.scalars(select(Section)).all()
    sections_schemas = [SectionSchema.model_validate(section) for section in sections]
    yield sections_schemas


@pytest.fixture(scope="session")
def streams(client: FlaskClient) -> Iterator[List[StreamSchema]]:
    streams = storage.session.scalars(select(Stream)).all()
    streams_schemas = [StreamSchema.model_validate(stream) for stream in streams]
    yield streams_schemas
