from fastapi import APIRouter, status
from fastapi.logger import logger
from fastapi.responses import JSONResponse
from sqlalchemy import text

from project.api.v1.routers.dependencies import SessionDep
from project.api.v1.routers.health.schema import HealthStatus

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
        session.execute(text("SELECT 1"))
        return HealthStatus(
            api_status="healthy",
            db_status="healthy",
        )
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "api_status": "healthy",
                "db_status": "unhealthy",
            },
        )
