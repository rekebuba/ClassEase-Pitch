from fastapi import APIRouter, HTTPException, status
from fastapi.logger import logger
from sqlalchemy import text

from project.api.v1.routers.dependencies import RedisDep, SessionDep
from project.api.v1.routers.health.schema import HealthStatus

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", response_model=HealthStatus)
async def get_health(session: SessionDep, redis: RedisDep) -> HealthStatus:
    """
    Returns the health status of the API.
    Checks the connectivity to the database and Redis.
    """
    db_ok = False
    redis_ok = False

    try:
        session.execute(text("SELECT 1"))
        db_ok = True

        redis_ok = await redis.ping()  # ty:ignore[invalid-await]

        if not redis_ok:
            raise Exception(
                "Redis health check failed: Unable to connect or ping Redis server."
            )

        return HealthStatus(
            api_status="healthy",
            db_status="healthy",
            redis_status="healthy",
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        # Raising an exception allows FastAPI to bypass the normal return validation
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "api_status": "healthy",
                "db_status": "healthy" if db_ok else "unhealthy",
                "redis_status": "healthy" if redis_ok else "unhealthy",
            },
        )
