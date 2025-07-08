from pydantic import BaseModel

from extension.pydantic.models.subject_schema import SubjectSchema


class SubjectResponse(BaseModel):
    """
    Schema for the list of subjects.
    """

    subjects: list[SubjectSchema] = []
