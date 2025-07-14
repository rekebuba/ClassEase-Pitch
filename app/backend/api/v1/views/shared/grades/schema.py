from typing import Optional, Any, Dict

from pydantic import (
    BaseModel,
    ConfigDict,
    model_validator,
)

from extension.functions.helper import to_camel


class GradeParams(BaseModel):
    """
    This model represents a grade in the system. It inherits from BaseModel.
    """

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: Optional[bool] = None
    year_id: Optional[bool] = None
    grade: Optional[bool] = None
    level: Optional[bool] = None
    has_stream: Optional[bool] = None

    @model_validator(mode="before")
    def check_at_least_one_field(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """a validator to ensure at least one field is requested"""
        if not any(data.values()):
            data["id"] = True
            data["grade"] = True
        return data
