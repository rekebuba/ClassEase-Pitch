from typing import List
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from project.api.v1.routers.dependencies import SessionDep
from project.api.v1.routers.health.schema import HealthStatus
from sqlalchemy import select


router = APIRouter(prefix="/health", tags=["Health"])

@router.get(
    "/",
    response_model=HealthStatus,
)
def get_health(
    session: SessionDep,
) -> HealthStatus | JSONResponse:
    """
    Returns the health status of the API
    """
    try:
        session.execute(select(1))
        return HealthStatus(
            api_status="healthy",
            db_status="healthy",
        )
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "api_status": "healthy",
                "db_status": "unhealthy",
            },
        )
