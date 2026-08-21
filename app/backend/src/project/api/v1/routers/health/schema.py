from project.schema.schema import BaseSchema


class HealthStatus(BaseSchema):
    api_status: str
    db_status: str
    redis_status: str
