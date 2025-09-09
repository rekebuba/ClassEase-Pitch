import uuid

from pydantic import BaseModel

from extension.pydantic.models.student_schema import StudentSchema


class RegistrationResponse(BaseModel):
    """
    Schema for successful registration response.
    """

    id: uuid.UUID


class StudentRegistrationForm(StudentSchema):
    pass
