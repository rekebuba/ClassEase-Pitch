from pydantic import BaseModel, ConfigDict

from project.utils.utils import to_camel


class HealthStatus(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    api_status: str
    db_status: str
    redis_status: str
