from fastapi import APIRouter

# from api.v1.routers.admin.post import router as admin_post_router
from api.v1.routers.grades import route as grade_router
from api.v1.routers.login import route as auth_router
from api.v1.routers.private import route as private_router
from api.v1.routers.registrations import route as registration_router
from api.v1.routers.sections import route as section_router
from api.v1.routers.streams import route as stream_router
from api.v1.routers.subjects import route as subject_router
from api.v1.routers.year import route as year_router

# Create a root router for v1
api_router = APIRouter()

# Include each sub-router
api_router.include_router(auth_router.router)
api_router.include_router(registration_router.router)
api_router.include_router(year_router.router)
api_router.include_router(grade_router.router)
api_router.include_router(subject_router.router)
api_router.include_router(stream_router.router)
api_router.include_router(section_router.router)
api_router.include_router(private_router.router)
