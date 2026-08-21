from fastapi import APIRouter

from project.api.v1.routers.academic_setup import route as academic_setup_router
from project.api.v1.routers.academic_term import route as academic_term_router
from project.api.v1.routers.auth import route as auth_router
from project.api.v1.routers.departments import route as departments_router
from project.api.v1.routers.employee import route as employee_router
from project.api.v1.routers.grades import route as grade_router
from project.api.v1.routers.health import route as health_router
from project.api.v1.routers.jobs import route as jobs_router
from project.api.v1.routers.positions import route as positions_router
from project.api.v1.routers.registrations import route as registration_router
from project.api.v1.routers.school import route as school_router
from project.api.v1.routers.sections import route as section_router
from project.api.v1.routers.streams import route as stream_router
from project.api.v1.routers.students import route as student_router
from project.api.v1.routers.subjects import route as subject_router
from project.api.v1.routers.teachers import route as teachers_router
from project.api.v1.routers.users import route as user_router
from project.api.v1.routers.year import route as year_router

# Create a root router for v1
api_router = APIRouter()

# Include each sub-router
api_router.include_router(health_router.router)
api_router.include_router(auth_router.router)
api_router.include_router(school_router.router)
api_router.include_router(registration_router.router)
api_router.include_router(year_router.router)
api_router.include_router(grade_router.router)
api_router.include_router(subject_router.router)
api_router.include_router(stream_router.router)
api_router.include_router(section_router.router)
api_router.include_router(user_router.router)
api_router.include_router(student_router.router)
api_router.include_router(employee_router.router)
api_router.include_router(teachers_router.router)
api_router.include_router(academic_term_router.router)
api_router.include_router(academic_setup_router.router)
api_router.include_router(jobs_router.router)
api_router.include_router(departments_router.router)
api_router.include_router(positions_router.router)
