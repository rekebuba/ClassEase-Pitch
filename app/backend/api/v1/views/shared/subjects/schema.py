from pydantic import BaseModel


class SubjectList(BaseModel):
    """
    Schema for the list of subjects.
    """

    subjects: list[str] = []
