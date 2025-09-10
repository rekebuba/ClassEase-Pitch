import uuid

from pydantic import BaseModel

from schema.models.student_schema import StudentSchema


class RegistrationResponse(BaseModel):
    """
    Schema for successful registration response.
    """

    id: uuid.UUID


class StudentRegistrationForm(StudentSchema):
    pass
