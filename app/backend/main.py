#!/usr/bin/python3
"""Main module for the API"""

import json
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from api.v1 import api_router
from core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.include_router(api_router, prefix="/api/v1")


# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)


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
    print("Caught a ResponseValidationError!")
    print(json.dumps(jsonable_encoder(exc.errors()), indent=2, sort_keys=True))
    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal server error due to response validation failure."
        },
    )
