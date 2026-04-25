#!/usr/bin/python3
"""Main module for the API"""

from fastapi import FastAPI, Request
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from project.api.v1 import api_router
from project.core.config import settings
from project.core.tenant import (
    TenantContextTokens,
    reset_tenant_context,
    resolve_school_slug_from_request,
    set_current_membership_id,
    set_current_school_id,
    set_request_school_slug,
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    redirect_slashes=False,
    docs_url=None
    if settings.ENVIRONMENT == "production"
    else f"{settings.API_V1_STR}/docs",
    redoc_url=None
    if settings.ENVIRONMENT == "production"
    else f"{settings.API_V1_STR}/redoc",
)

app.include_router(api_router, prefix=settings.API_V1_STR)


# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,  # ty:ignore[invalid-argument-type]
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.middleware("http")
async def tenant_context_middleware(request: Request, call_next):
    tokens = TenantContextTokens(
        school_id=set_current_school_id(None),
        membership_id=set_current_membership_id(None),
        school_slug=set_request_school_slug(resolve_school_slug_from_request(request)),
    )
    try:
        response = await call_next(request)
    finally:
        reset_tenant_context(tokens)
    return response


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name


use_route_names_as_operation_ids(app)


@app.exception_handler(ResponseValidationError)
async def validation_exception_handler(
    request: Request, exc: ResponseValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal server error due to response validation failure."
        },
    )
